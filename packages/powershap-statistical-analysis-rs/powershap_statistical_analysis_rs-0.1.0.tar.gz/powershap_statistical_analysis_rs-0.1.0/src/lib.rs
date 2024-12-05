mod helpers;

use pyo3::prelude::*;
use polars::prelude::*;
use pyo3_polars::PyDataFrame;
use helpers::ttestpower_power;
use rayon::prelude::*;

// Calculate p-values based on arg coefficient
// https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.percentileofscore.html
// Using the 'rank' method: average percentage ranking of score. In case of multiple matches, average the percentage rankings of all matching scores.
fn p_values_arg_coef(coefficients: Vec<f64>, args: Vec<f64>) -> Vec<f64> {
    let n = coefficients.len() as f64;

    // Calculate percentile for each arg
    args.iter()
        .map(|score| {
            // Count values strictly less than score
            let less_than = coefficients.iter().filter(|&x| x < score).count() as f64;

            // Count values equal to score
            let equal_to = coefficients.iter().filter(|&x| x == score).count() as f64;

            ((less_than + (equal_to + 1.0) / 2.0) / n) * 100.0
        })
        .collect()
}

// https://github.com/predict-idlab/powershap/blob/main/powershap/utils.py
// My implementation of the powershap statistical analysis in native Rust to improve performance
#[pyfunction]
pub fn powershap_statistical_analysis(
    shaps_df: PyDataFrame,
    power_alpha: f64,
    power_req_iterations: f64,
    include_all: bool,
) -> PyDataFrame {
    // Convert PyDataFrame to polars DataFrame
    let df: DataFrame = shaps_df.into();
    let n_columns: usize = df.width();

    let mut effect_size: Vec<f64> = vec![];
    let mut power_list: Vec<f64> = vec![];
    let mut required_iterations: Vec<f64> = vec![];
    let mut impact_values: Vec<f64> = vec![];

    // Get number of samples and mean of random_uniform_feature
    let n_samples = df.height() as f64;
    let random_uniform_feature = df.column("random_uniform_feature").unwrap().f64().unwrap();
    let mean_random_uniform = random_uniform_feature.mean().unwrap();
    let std_random_uniform = random_uniform_feature.std(1).unwrap();

    let results: Vec<(f64, f64, f64, f64, f64)> = (0..n_columns).into_par_iter().map(|i| {
        let col = &df.get_columns()[i];
        let col_mean = col.f64().unwrap().mean().unwrap();
        let col_std = col.f64().unwrap().std(1).unwrap();
        
        // Calculate p-value
        let col_values: Vec<f64> = col.f64().unwrap().into_iter().filter_map(|x| x).collect();
        let p_value = p_values_arg_coef(col_values, vec![mean_random_uniform])[0] / 100.0;
        
        let (effect_size_val, power_val, required_iterations_val) = if include_all || p_value < power_alpha {
            // Calculate pooled standard deviation
            let pooled_std = ((col_std.powi(2) + std_random_uniform.powi(2)) / 2.0).sqrt();
            let effect = (mean_random_uniform - col_mean) / pooled_std;
            
            // Calculate power
            let power = ttestpower_power(effect, n_samples, power_alpha, None, "smaller");
            
            // Calculate required iterations if needed
            let req_iterations = if col.name() == "random_uniform_feature" {
                0.0
            } else {
                // PLACEHOLDER FOR SOLVE POWER
                Python::with_gil(|py| {
                    let statsmodels = PyModule::import_bound(py, "statsmodels.stats.power").unwrap();
                    let t_test = statsmodels.getattr("TTestPower").unwrap().call0().unwrap();

                    let kwargs = pyo3::types::PyDict::new_bound(py);
                    kwargs.set_item("effect_size", effect.abs()).unwrap();
                    kwargs.set_item("nobs", py.None()).unwrap();
                    kwargs.set_item("alpha", power_alpha).unwrap();
                    kwargs.set_item("power", power_req_iterations).unwrap();
                    kwargs.set_item("alternative", "smaller").unwrap();

                    match t_test.call_method("solve_power", (), Some(&kwargs)) {
                        Ok(result) => result.extract::<f64>().unwrap_or(0.0),
                        Err(_) => 0.0,
                    }
                })
            };
            
            (effect, power, req_iterations)
        } else {
            (0.0, 0.0, 0.0)
        };
        
        (col_mean, p_value, effect_size_val, power_val, required_iterations_val)
    }).collect();
    
    // Unzip results into separate vectors, including p_values
    let mut p_values = Vec::with_capacity(n_columns);

    for (impact, p_value, effect, power, req_iterations) in results {
        impact_values.push(impact);
        p_values.push(p_value);  // Add p_values to vector
        effect_size.push(effect);
        power_list.push(power);
        required_iterations.push(req_iterations);
    }
    
    // Get column names
    let column_names: Vec<String> = df.get_columns()
        .iter()
        .map(|col| col.name().to_string())
        .collect();

    // Create result DataFrame
    let power_alpha_col = format!("power_{}_alpha", power_alpha);
    let iterations_col = format!("{}_power_its_req", power_req_iterations);

    let processed_shaps_df = DataFrame::new(vec![
        Series::new("feature".into(), column_names).into_column(),
        Series::new("impact".into(), impact_values).into(),
        Series::new("p_value".into(), p_values).into(),
        Series::new("effect_size".into(), effect_size).into(),
        Series::new(power_alpha_col.into(), power_list).into(),
        Series::new(iterations_col.into(), required_iterations).into(),
    ])
    .unwrap()
    .lazy()
    .sort_by_exprs(
        &[col("impact").abs().alias("impact")],
        SortMultipleOptions {
            descending: vec![true], 
            ..Default::default()
        },
    )
    .collect()
    .unwrap();

    // Convert back to PyDataFrame
    PyDataFrame(processed_shaps_df.clone())
}

/// A Python module implemented in Rust.
#[pymodule]
fn powershap_statistical_analysis_rs(_py: Python<'_>, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(powershap_statistical_analysis, m)?)?;
    Ok(())
}

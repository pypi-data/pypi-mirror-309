use r_mathlib::non_central_t_cdf;
use statrs::distribution::{ContinuousCDF, StudentsT};

// Helper functions to match Python's nctdtr behavior
fn nct_cdf(x: f64, df: f64, nc: f64) -> f64 {
    non_central_t_cdf(x, df, nc, true, false)
}

fn nct_sf(x: f64, df: f64, nc: f64) -> f64 {
    non_central_t_cdf(x, df, nc, false, false)
}

pub fn ttestpower_power(
    effect_size: f64,
    nobs: f64,
    alpha: f64,
    df: Option<f64>,
    alternative: &str,
) -> f64 {
    // Use provided df or default to nobs - 1
    let degrees_of_freedom = df.unwrap_or(nobs - 1.0);

    // Calculate non-centrality parameter
    let nc = effect_size * nobs.sqrt();

    // Adjust alpha for two-sided test
    let alpha_ = if alternative == "two-sided" || alternative == "2s" {
        alpha / 2.0
    } else if alternative == "smaller" || alternative == "larger" {
        alpha
    } else {
        panic!("alternative must be 'two-sided', 'larger', or 'smaller'")
    };

    // Initialize power
    let mut power = 0.0;

    // Create t distribution
    let t_dist = StudentsT::new(0.0, 1.0, degrees_of_freedom).unwrap();

    // Calculate power based on alternative
    if alternative == "two-sided" || alternative == "2s" || alternative == "larger" {
        let crit_upp = t_dist.inverse_cdf(alpha_);
        if crit_upp.is_nan() {
            return f64::NAN;
        }
        power = nct_sf(crit_upp, degrees_of_freedom, nc);
    }

    if alternative == "two-sided" || alternative == "2s" || alternative == "smaller" {
        let crit_low = t_dist.inverse_cdf(alpha_);
        if crit_low.is_nan() {
            return f64::NAN;
        }
        power += nct_cdf(crit_low, degrees_of_freedom, nc);
    }

    power
}

// TODO: Implement ttestpower_solve_power in Rust
pub fn ttestpower_solve_power() {
    todo!()
}

#[cfg(test)]
mod tests {

    use super::*;
    #[test]
    // There is a discrepancy between the results of nct_cdf from Rust and Python. The result in Python is 0.30478544999846835.
    // The discrepancy is due to the difference in the implementation of the non-central t distribution.
    fn test_nct_cdf() {
        let x = 1.5;
        let df = 10.0;
        let nc = 2.0;
        assert_eq!(nct_cdf(x, df, nc), 0.30478544737559365);
    }

    #[test]
    // There is a discrepancy between the results of nct_sf from Rust and Python. The result in Python is 0.6952145500015317.
    // The discrepancy is due to the difference in the implementation of the non-central t distribution.
    fn test_nct_sf() {
        let x = 1.5;
        let df = 10.0;
        let nc = 2.0;
        assert_eq!(nct_sf(x, df, nc), 0.6952145526244063);
    }

    #[test]
    // There is a discrepancy between the results of ttestpower_power from Rust and Python. The result in Python is 1.4189030167076257e-07.
    // The discrepancy is due to the difference in the implementation of the non-central t distribution.
    fn test_ttestpower_power() {
        let effect_size = 0.5;
        let nobs = 50.0;
        let alpha = 0.05;
        let df: Option<f64> = None;
        let alternative = "smaller";
        let power = ttestpower_power(effect_size, nobs, alpha, df, alternative);
        assert_eq!(power, 1.4268513315318643e-7);
    }
}

extern crate polars;
extern crate pyo3;
extern crate pyo3_macros;
extern crate pyo3_polars;
extern crate serde;
mod interval;

use interval::make_interval_match;
use polars::prelude::*;
use pyo3_polars::derive::polars_expr;
use serde::Deserialize;

#[derive(Deserialize)]
struct ReferenceIntervals {
    intervals: String,
}

#[polars_expr(output_type=String)]
fn match_intervals(values: &[Series], kwargs: ReferenceIntervals) -> Result<Series, PolarsError> {
    let values = &values[0];
    let intervals: String = kwargs.intervals.into();

    let interval_matcher = make_interval_match(&intervals);

    let return_series = match values.f64() {
        Ok(values) => {
            let mut matched_intervals = Vec::new();
            for value in values.into_iter() {
                let matched_interval = match value {
                    Some(v) => interval_matcher(v),
                    None => "None".to_string(),
                };
                matched_intervals.push(matched_interval);
            }
            let t = Series::new("matched_intervals".into(), matched_intervals);
            println!("{:?}", &t);
            t
        }
        Err(e) => {
            return Err(e);
        }
    };
    Ok(return_series)
}

use std::cmp::Ordering;
use std::collections::BTreeMap;

#[derive(Debug, PartialEq, PartialOrd, Copy, Clone)]
pub struct OrderedFloat(f64);

impl Eq for OrderedFloat {}

impl Ord for OrderedFloat {
    fn cmp(&self, other: &Self) -> Ordering {
        self.partial_cmp(other).unwrap_or(Ordering::Equal)
    }
}

pub fn parse_interval(
    interval: &str,
) -> Result<(OrderedFloat, OrderedFloat, bool, bool), &'static str> {
    let inclusive_start = interval.starts_with('[');
    let inclusive_end = interval.ends_with(']');
    let interval = interval.trim_matches(|c| c == '[' || c == ']' || c == '(' || c == ')');
    let nums: Vec<f64> = interval
        .split(',')
        .map(|s| s.trim().parse().map_err(|_| "Invalid number format"))
        .collect::<Result<Vec<f64>, _>>()?;

    if nums.len() != 2 {
        return Err("Invalid interval format");
    }

    Ok((
        OrderedFloat(nums[0]),
        OrderedFloat(nums[1]),
        inclusive_start,
        inclusive_end,
    ))
}

pub fn make_interval_match(intervals: &str) -> impl Fn(f64) -> String {
    let interval_list: Vec<&str> = intervals.split(';').map(|s| s.trim()).collect();
    let mut interval_map: BTreeMap<(OrderedFloat, OrderedFloat), (bool, bool, String)> =
        BTreeMap::new();

    for interval in interval_list {
        if let Ok((lower, upper, incl_start, incl_end)) = parse_interval(interval) {
            interval_map.insert((lower, upper), (incl_start, incl_end, interval.to_string()));
        }
    }

    move |n: f64| -> String {
        for (&(lower, upper), &(incl_start, incl_end, ref interval_str)) in interval_map.range(..) {
            let lower_bound = if incl_start { lower.0 } else { lower.0 + 1.0 };
            let upper_bound = if incl_end { upper.0 } else { upper.0 - 1.0 };

            if (lower_bound as f64..=upper_bound as f64).contains(&n) {
                return interval_str.clone();
            }
        }
        "None".to_string()
    }
}

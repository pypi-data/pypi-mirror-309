use polars::prelude::*;
use chrono::NaiveDate;
use postgres_openssl::MakeTlsConnector;
use openssl::ssl::{SslConnector, SslMethod};
use postgres::Client;
use pyo3::prelude::*;
use pyo3_polars::PyDataFrame;

#[pyfunction]
fn load_data_from_postgresql(
    table_name: &str, 
    date_column: &str, 
    country: &str, 
    host: &str, 
    port: u16, 
    user: &str, 
    password: &str, 
    database: &str
) -> PyDataFrame {

    // Set up SSL connector
    let mut builder = SslConnector::builder(SslMethod::tls()).unwrap();
    builder.set_verify(openssl::ssl::SslVerifyMode::NONE); // Disable certificate verification (development only)
    let connector = MakeTlsConnector::new(builder.build());

    // Connect with SSL
    let mut client = Client::connect(
        &format!(
            "host={} port={} user={} password={} dbname={}",
            host, port, user, password, database
        ),
        connector
    ).unwrap();


    let query = format!("SELECT * FROM {} WHERE country = $1", table_name);
    let rows = client.query(&query, &[&country]).unwrap();

    // Convert rows to vectors for each column
    let mut dates = Vec::new();
    let mut spending = Vec::new();
    let mut countries = Vec::new();

    for row in rows {
        let date: NaiveDate = row.get(0); // Get date directly as NaiveDate
        dates.push(date);
    
        spending.push(row.get::<_, i64>(1));
        countries.push(row.get::<_, String>(2));
    }

    // Create series for each column
    let date_series = Series::new(date_column.into(), dates);
    let spending_series = Series::new(table_name.into(), spending);
    let country_series = Series::new("country".into(), countries);

    // Create DataFrame
    let df = DataFrame::new(vec![date_series.into(), spending_series.into(), country_series.into()]).unwrap();
    
    PyDataFrame(df)
}

#[pymodule]
fn load_data_from_postgresql_rs(_py: Python<'_>, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(load_data_from_postgresql, m)?)?;
    Ok(())
}
#[macro_use] extern crate rocket;

use rocket::http::Status;
use rocket::serde::json::{json, Json, Value};

fn spark_url() -> String {
    std::env::var("SPARK_URL").unwrap_or_else(|_| "http://127.0.0.1:9000".into())
}

fn pod_name() -> String {
    std::env::var("HOSTNAME").unwrap_or_else(|_| "unknown".into())
}

#[get("/")]
fn index() -> String {
    format!("Hello from Rocket (Rust)! Served by: {}\n", pod_name())
}

#[get("/students")]
async fn students() -> Result<Json<Value>, Status> {
    let url = format!("{}/students", spark_url());
    let resp = reqwest::get(&url).await.map_err(|_| Status::BadGateway)?;
    let data: Value = resp.json().await.map_err(|_| Status::BadGateway)?;
    Ok(Json(json!({ "served_by": pod_name(), "source": "Spark SQL", "data": data })))
}

#[launch]
fn rocket() -> _ {
    rocket::build().mount("/", routes![index, students])
}

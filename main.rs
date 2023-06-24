use std::fs;
use std::fs::File;
use std::io::prelude::*;
use std::path::{Path, PathBuf};
use exif::{DateTime, Reader, Tag, Value};
use geocoding::geocoder::Geocoder;
use geocoding::types::Location;

fn is_img(file: &Path) -> bool {
    let extension = file.extension().and_then(|ext| ext.to_str());
    if let Some(ext) = extension {
        return ext.eq_ignore_ascii_case("jpg") || ext.eq_ignore_ascii_case("jpeg") || ext.eq_ignore_ascii_case("png");
    }
    false
}

fn exif_collect(img: &exif::Exif, file: &Path) -> Option<String> {
    let name = file.file_name()?.to_string_lossy().into_owned();
    let file_format = file.extension()?.to_string_lossy().into_owned();

    let date = img.get_field(Tag::DateTime, false)?.value.display_as(Tag::DateTime).to_string();
    let date_parts: Vec<&str> = date.split(" ").collect();
    let date = date_parts[0].replace(":", "-");

    let latitude = img.get_field(Tag::GPSLatitude, false)?.value.clone();
    let longitude = img.get_field(Tag::GPSLongitude, false)?.value.clone();

    let location = get_location(&latitude, &longitude)?;

    let img_data = format!(
        "name: {}\nformat: {}\ndate: {}\nlocation: {}",
        name, file_format, date, location
    );

    Some(img_data)
}

fn get_location(latitude: &Value, longitude: &Value) -> Option<String> {
    let geocoder = Geocoder::new();

    if let (Value::Rational(lat_components), Value::Rational(lon_components)) = (latitude, longitude) {
        let lat_value = lat_components.value[0].to_f64()? + (lat_components.value[1].to_f64()? / 60.0)
            + (lat_components.value[2].to_f64()? / 3600.0);
        let lon_value = lon_components.value[0].to_f64()? + (lon_components.value[1].to_f64()? / 60.0)
            + (lon_components.value[2].to_f64()? / 3600.0);

        let location = geocoder.reverse(&Location {
            latitude: lat_value,
            longitude: lon_value,
        })?;

        let location_string = format!("{}_{}", location.country, location.city);
        return Some(location_string);
    }

    None
}

fn pictures_sort(folder: &Path) {
    let files = fs::read_dir(folder).unwrap();

    let others_dir = folder.join("others");
    let need_to_sort_dir = folder.join("need_to_sort");

    if !others_dir.exists() {
        fs::create_dir(&others_dir).unwrap();
    }

    if !need_to_sort_dir.exists() {
        fs::create_dir(&need_to_sort_dir).unwrap();
    }

    for entry in files.filter_map(Result::ok) {
        let path = entry.path();

        if let Ok(metadata) = fs::metadata(&path) {
            if metadata.is_file() && is_img(&path) {
                let file_name = path.file_name().unwrap().to_string_lossy().into_owned();

                let mut file = File::open(&path).unwrap();
                let mut buffer = Vec::with_capacity(metadata.len() as usize);
                file.read_to_end(&mut buffer).unwrap();

                let exif_reader = Reader::new();
                let exif = exif_reader.read_from_container(&buffer).unwrap();

                if let Some(img_data) = exif_collect(&exif, &path) {
                    let new_file_name = format!("{}_{}_{}", img_data.location, img_data.date, file_name);
                    let new_file_path = folder.join(&new_file_name);
                    fs::rename(&path, &new_file_path).unwrap();

                    println!("File sorted!");
                }
            } else {
                let dest_path = others_dir.join(path.file_name().unwrap());
                fs::rename(&path, &dest_path).unwrap();

                pictures_sort(&others_dir);
            }
        }
    }

    println!("All files are sorted!");
}

fn main() {
    let folder_src = std::env::args().nth(1).expect("Please provide the folder path as an argument.");
    let folder_path = PathBuf::from(&folder_src);

    pictures_sort(&folder_path);
}
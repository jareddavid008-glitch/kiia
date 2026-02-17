import requests
import csv

def get_ip_location(ip=""):
    url = f"http://ip-api.com/json/{ip}?fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,mobile,proxy,hosting,query"
    
    try:
        r = requests.get(url, timeout=6)
        data = r.json()
        
        if data.get("status") != "success":
            return {"error": data.get("message", "failed")}
        
        return {
            "ip": data["query"],
            "country": data["country"],
            "country_code": data["countryCode"],
            "region": data["regionName"],
            "city": data["city"],
            "zip": data["zip"],
            "lat": data["lat"],
            "lon": data["lon"],
            "timezone": data["timezone"],
            "isp": data["isp"],
            "org": data["org"],
            "as": data["as"],
            "is_mobile": data["mobile"],
            "is_proxy_vpn_tor": data["proxy"] or data["hosting"]
        }
    except Exception as e:
        return {"error": str(e)}

ip_data = get_ip_location("103.157.240.53")
csv_file = "ip_location_data.csv"

if "error" not in ip_data:
    
    fieldnames = [
        "ip", "country", "country_code", "region", "city", "zip", "lat", "lon",
        "timezone", "isp", "org", "as", "is_mobile", "is_proxy_vpn_tor"
    ]
    
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(ip_data)

    print(f"Data has been written to {csv_file}")
else:
    print(f"Error: {ip_data['error']}")

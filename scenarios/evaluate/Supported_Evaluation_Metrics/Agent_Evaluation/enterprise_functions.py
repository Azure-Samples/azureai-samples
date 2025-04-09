import os
import json
import requests
from datetime import datetime as pydatetime, timedelta, timezone
from typing import Optional, Callable, Any, Set
from dotenv import load_dotenv

load_dotenv()


def fetch_datetime(
    format_str: str = "%Y-%m-%d %H:%M:%S", unix_ts: int | None = None, tz_offset_seconds: int | None = None
) -> str:
    """
    Returns either the current UTC date/time in the given format, or if unix_ts
    is given, converts that timestamp to either UTC or local time (tz_offset_seconds).

    :param format_str: The strftime format, e.g. "%Y-%m-%d %H:%M:%S".
    :param unix_ts: Optional Unix timestamp. If provided, returns that specific time.
    :param tz_offset_seconds: If provided, shift the datetime by this many seconds from UTC.
    :return: A JSON string containing the "datetime" or an "error" key/value.
    """
    try:
        if unix_ts is not None:
            dt_utc = pydatetime.fromtimestamp(unix_ts, tz=timezone.utc)
        else:
            dt_utc = pydatetime.now(timezone.utc)

        if tz_offset_seconds is not None:
            local_tz = timezone(timedelta(seconds=tz_offset_seconds))
            dt_local = dt_utc.astimezone(local_tz)
            result_str = dt_local.strftime(format_str)
        else:
            result_str = dt_utc.strftime(format_str)

        return json.dumps({"datetime": result_str})
    except Exception as e:
        return json.dumps({"error": f"Exception: {e!s}"})


def fetch_weather(
    location: str,
    country_code: str = "",
    state_code: str = "",
    limit: int = 1,
    timeframe: str = "current",
    time_offset: int = 0,
    dt_unix: Optional[int] = None,
) -> str:
    """
    Fetches weather data from OpenWeather for the specified location and timeframe.

    :param location: The city or place name to look up.
    :param country_code: (optional) e.g. 'US' or 'GB' to narrow down your search.
    :param state_code: (optional) The state or province code, e.g. 'CA' for California.
    :param limit: (optional) The max number of geocoding results (defaults to 1).
    :param timeframe: The type of weather data, e.g. 'current','hourly','daily','timemachine', or 'overview'.
    :param time_offset: For 'hourly' or 'daily', used as the index into the array. For 'overview', the day offset.
    :param dt_unix: A Unix timestamp, required if timeframe='timemachine'.
    :return: A JSON string containing weather data or an "error" key if an issue.
    """
    try:
        if not location:
            return json.dumps({"error": "Missing required parameter: location"})

        geo_api_key = os.environ.get("OPENWEATHER_GEO_API_KEY")
        one_api_key = os.environ.get("OPENWEATHER_ONE_API_KEY")
        if not geo_api_key or not one_api_key:
            return json.dumps({"error": "Missing OpenWeather API keys in environment."})

        # Convert location -> lat/lon:
        if country_code and state_code:
            query = f"{location},{state_code},{country_code}"
        elif country_code:
            query = f"{location},{country_code}"
        else:
            query = location

        geocode_url = f"http://api.openweathermap.org/geo/1.0/direct?" f"q={query}&limit={limit}&appid={geo_api_key}"
        geo_resp = requests.get(geocode_url)
        if geo_resp.status_code != 200:
            return json.dumps(
                {"error": "Geocoding request failed", "status_code": geo_resp.status_code, "details": geo_resp.text}
            )

        geocode_data = geo_resp.json()
        if not geocode_data:
            return json.dumps({"error": f"No geocoding results for '{location}'."})

        lat = geocode_data[0].get("lat")
        lon = geocode_data[0].get("lon")
        if lat is None or lon is None:
            return json.dumps({"error": "No valid lat/long returned."})

        tf = timeframe.lower()
        if tf == "timemachine":
            if dt_unix is None:
                return json.dumps({"error": "For timeframe='timemachine', you must provide 'dt_unix'."})
            url = (
                f"https://api.openweathermap.org/data/3.0/onecall/timemachine"
                f"?lat={lat}&lon={lon}"
                f"&dt={dt_unix}"
                f"&units=metric"
                f"&appid={one_api_key}"
            )
        elif tf == "overview":
            date_obj = pydatetime.utcnow() + timedelta(days=time_offset)
            date_str = date_obj.strftime("%Y-%m-%d")
            url = (
                f"https://api.openweathermap.org/data/3.0/onecall/overview?"
                f"lat={lat}&lon={lon}"
                f"&date={date_str}"
                f"&units=metric"
                f"&appid={one_api_key}"
            )
        else:
            if tf == "current":
                exclude = "minutely,hourly,daily,alerts"
            elif tf == "hourly":
                exclude = "minutely,daily,alerts"
            elif tf == "daily":
                exclude = "minutely,hourly,alerts"
            else:
                exclude = ""

            url = (
                f"https://api.openweathermap.org/data/3.0/onecall?"
                f"lat={lat}&lon={lon}"
                f"&exclude={exclude}"
                f"&units=metric"
                f"&appid={one_api_key}"
            )

        resp = requests.get(url)
        if resp.status_code != 200:
            return json.dumps({"error": "Weather API failed", "status_code": resp.status_code, "details": resp.text})

        data = resp.json()
        if tf == "overview":
            overview = data.get("weather_overview", "No overview text provided.")
            return json.dumps(
                {
                    "location": location,
                    "latitude": lat,
                    "longitude": lon,
                    "weather_overview": overview,
                    "description": "N/A",
                    "temperature_c": "N/A",
                    "temperature_f": "N/A",
                    "humidity_percent": "N/A",
                }
            )

        if tf == "timemachine":
            arr = data.get("data", [])
            if not arr:
                return json.dumps({"error": "No 'data' array for timemachine"})
            sel = arr[0]
        elif tf == "hourly":
            arr = data.get("hourly", [])
            if time_offset < 0 or time_offset >= len(arr):
                return json.dumps({"error": f"Requested hour index {time_offset}, but length is {len(arr)}"})
            sel = arr[time_offset]
        elif tf == "daily":
            arr = data.get("daily", [])
            if time_offset < 0 or time_offset >= len(arr):
                return json.dumps({"error": f"Requested day index {time_offset}, but length is {len(arr)}"})
            sel = arr[time_offset]
        else:
            sel = data.get("current", {})

        if not isinstance(sel, dict):
            return json.dumps({"error": f"Unexpected data format for timeframe={timeframe}"})

        description = "N/A"
        if sel.get("weather"):
            description = sel["weather"][0].get("description", "N/A")

        temp_c = sel.get("temp")
        humidity = sel.get("humidity", "N/A")
        if isinstance(temp_c, (int, float)):
            temp_f = round(temp_c * 9 / 5 + 32, 2)
        else:
            temp_f = "N/A"

        result = {
            "location": location,
            "latitude": lat,
            "longitude": lon,
            "description": description,
            "temperature_c": temp_c if temp_c is not None else "N/A",
            "temperature_f": temp_f,
            "humidity_percent": humidity,
        }
        return json.dumps(result)
    except Exception as e:
        return json.dumps({"error": f"Exception occurred: {e!s}"})


def fetch_stock_price(
    ticker_symbol: str, period: str = "1d", interval: str = "1d", start: Optional[str] = None, end: Optional[str] = None
) -> str:
    """
    Fetch stock price info for a given ticker symbol, with optional historical data.

    :param ticker_symbol: The ticker symbol to look up, e.g. "MSFT".
    :param period: Over what period to pull data, e.g. "1d", "1mo", "1y".
    :param interval: The granularity of data, e.g. "1d", "1h".
    :param start: (optional) The start date/time in YYYY-MM-DD or YYYY-MM-DD HH:MM:SS format.
    :param end: (optional) The end date/time in similar format.
    :return: A JSON string containing stock data or an "error" message.
    """
    import yfinance as yf

    try:
        stock = yf.Ticker(ticker_symbol)
        stock_data = stock.history(period=period, interval=interval, start=start, end=end)
        if stock_data.empty:
            return json.dumps({"error": f"No data found for symbol: {ticker_symbol}"})

        stock_data.reset_index(inplace=True)
        stock_data["Date"] = stock_data["Date"].dt.strftime("%Y-%m-%d %H:%M:%S")
        data_records = stock_data.to_dict(orient="records")

        return json.dumps({"ticker_symbol": ticker_symbol.upper(), "data": data_records})
    except (KeyError, ValueError) as e:
        return json.dumps({"error": f"Invalid or missing data: {e}"})
    except Exception as e:
        return json.dumps({"error": f"Unexpected issue - {type(e).__name__}: {e}"})


def send_email(recipient: str, subject: str, body: str) -> str:
    """
    Sends an email to the user-instructed mailbox using an Azure Logic App HTTP trigger e.g., {"recipient":string,"subject":string,"body":string}).

    :param recipient: The email address to send the email to.
    :param subject: The subject line of the email.
    :param body: The content within the email body.
    :return: A JSON string with either a "message" or an "error" key.
    """
    # Retrieve the Logic App URL from the environment.
    logic_app_url = os.getenv("LOGIC_APP_SEND_EMAIL_URL")
    if not logic_app_url:
        return json.dumps({"error": "Logic App endpoint URL is not configured in the environment."})

    # Construct the payload to match the Logic App's expected schema.
    payload = {"recipient": recipient, "subject": subject, "body": body}

    try:
        # Make the POST request to the Logic App.
        response = requests.post(logic_app_url, json=payload)
        response.raise_for_status()  # Raise an exception for any HTTP errors.

        # Attempt to parse the JSON response from the Logic App.
        try:
            response_data = response.json()
        except Exception:
            response_data = response.text

        return json.dumps({"message": f"Email sent to {recipient}.", "response": response_data})
    except requests.exceptions.HTTPError as http_err:
        return json.dumps({"error": f"HTTP error occurred: {http_err}", "details": response.text})
    except Exception as e:
        return json.dumps({"error": f"An error occurred: {e!s}"})


# make functions callable a callable set from enterprise-streaming-agent.ipynb
enterprise_fns: Set[Callable[..., Any]] = {
    fetch_datetime,
    fetch_weather,
    fetch_stock_price,
    # send_email
}

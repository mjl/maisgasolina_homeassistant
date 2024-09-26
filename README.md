# maisgasolina_homeassistant

Scrape fuel prices from *maisgasolina.pt* for use in home assistant

## Usage

Copy `maisgasolina.py` to `python_scripts` directory (or actually anywhere) in the home assistant environment.

Find the station of interest on https://www.maisgasolina.com/, extract the station id from the page url

Add to `configuration.yaml`:

```yaml
command_line:
  - sensor:
      name: Rio Maior Gasoleo
      command: "python3 python_scripts/maisgasolina.py -s 123 -p diesel"

      json_attributes:
        - updated
        - station_name
      value_template: "{{ value_json.price }}"

      unit_of_measurement: "€"
      state_class: measurement
      device_class: monetary
      scan_interval: 14400
      icon: mdi:gas-station

```

## Result stucture

% python maisgasolina.py -s 123

{"status": "OK", "station": 123, "product": "diesel", "source": "https://www.maisgasolina.com/posto/123/", "station_name": "BP - A15 Rio Maior S", "price": "1.684", "updated": "Pre\u00e7os actualizados a 24 de Setembro de 2024 por tumbas"}


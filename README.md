# maisgasolina_homeassistant
Scrape fuel prices from maisgasolina.pt for use in home assistant

Copy maisgasolina.py to python_scripts directory (or actually anywhere) in the home assistant environment.

Add to `...yaml`:

```yaml
command_line:
  - sensor:
      name: Intermarche Vila Verde Gasoleo
      command: "python3 python_scripts/maisgasolina.py -s 995 -p diesel"
      unit_of_measurement: "€"
      state_class: measurement
      device_class: monetary
      scan_interval: 14400
      icon: mdi:gas-station
```



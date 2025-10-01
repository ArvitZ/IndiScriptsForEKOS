# KStars EKOS Astronomy Automation Scripts

This project provides a my personal set of Python scripts and utilities for automating my astrophotography sessions using KStars EKOS and INDI drivers. The system manages telescope setup, camera cooling, dust cap control, flat field calibration, and automated imaging sequences sofar.

## Features

- **Automated Observatory Setup**: Startup and shutdown scripts for complete session management
- **Dust Cap Control**: Automated dust cap parking/unparking with integrated flat panel
- **Auto-Focus Integration**: Preset focus positions for different imaging sessions
- **Flat Field Automation**: Separate scripts for RGB and narrowband flat calibration
- **Camera Cooling**: Automatic camera temperature control (currently fixed at -5°C)
- **INDI Device Management**: Direct control of telescope, camera, focuser, and accessories
- **EKOS Sequence Templates**: Pre-configured capture sequences for various imaging scenarios
- **Custom Hardware Support**: Specialized driver for RBF Excalibur dust cap/flat panel

## Hardware Requirements

This automation system is designed for the following equipment setup:

- **Telescope Mount**: LX200 OnStep compatible mount
- **Camera**: Cooled astronomical CCD/CMOS camera
- **Auto-Focuser**: ToupTek AAF 2 focuser
- **Dust Cap/Flat Panel**: RBF Excalibur 
- **Software**: KStars/EKOS with INDI server

## Prerequisites

### Software Dependencies
```bash
# Required Python packages
pip install PyIndi
pip install dbus-python
pip install gobject

# System packages (Ubuntu/Debian)
sudo apt-get install kstars-bleeding
sudo apt-get install indi-full
sudo apt-get install python3-dbus
sudo apt-get install python3-gi
```

### INDI Server Setup
Ensure your INDI server includes the necessary drivers:
```bash
indiserver indi_lx200_OnStep indi_simulator_ccd indi_touptek_aaf indi_excalibur
```

## Project Structure

```
scripts/
├── indiClientAZ.py          # Core INDI client class for device communication
├── startup.py               # Session startup automation (uncap, focus, cool)
├── shutdown.py              # Session shutdown automation (park cap, warm up)
├── start_flat_RGB.py        # RGB flat field capture setup (brightness: 20)
├── start_flat_NB7.py        # Narrowband flat field setup (brightness: 500)
├── ekos-templates/          # EKOS sequence files (.esq)
│   ├── flats_RGB.esq        # RGB flat field sequence
│   ├── flats_RGB_v2.esq     # Alternative RGB flat sequence
│   ├── flats_HaO3.esq       # Ha/OIII flat sequence
│   ├── flats_S2O3.esq       # SII/OIII flat sequence
│   ├── lights_120s_RGB.esq  # 120s RGB light frames
│   └── lights_300s_HaO3.esq # 300s narrowband light frames
└── sources/                 # Source code and documentation
    ├── Excalibur.cpp        # Custom INDI driver for RBF Excalibur
    ├── Excalibur.h          # Driver header file
    ├── uncap.py             # D-Bus script for dust cap control
    └── indi_server_output.md # INDI server connection logs
```

## Usage Guide

### Session Startup
Begin your imaging session with the startup script:
```bash
python3 startup.py
```
This script will:
- Connect to local INDI server (port 7624)
- Move focuser to preset position (11,000 steps)
- Unpark the dust cap
- Cool camera to -5°C (if configured)

### Flat Field Calibration

**For RGB Imaging:**
```bash
python3 start_flat_RGB.py
```
- Parks dust cap to enable flat panel
- Sets flat panel brightness to 20 (optimal for RGB)
- Activates flat panel illumination

**For Narrowband Imaging:**
```bash
python3 start_flat_NB7.py  
```
- Parks dust cap to enable flat panel
- Sets flat panel brightness to 500 (optimal for narrowband filters)
- Activates flat panel illumination

### Session Shutdown
End your session safely:
```bash
python3 shutdown.py
```
This script will:
- Move focuser to park position (0 steps)
- Park the dust cap for protection
- Warm up camera (if configured)

### EKOS Sequence Integration

Load the appropriate sequence file in EKOS:

1. **RGB Imaging**: Use `lights_120s_RGB.esq` for 2-minute exposures
2. **Narrowband**: Use `lights_300s_HaO3.esq` for 5-minute exposures  
3. **Flat Fields**: Use corresponding flat sequences after running flat setup scripts

## Configuration

### Device Settings
Edit the scripts to match your hardware configuration:

```python
# In startup.py and shutdown.py
TARGET_FOCUS_POS = 11000  # Adjust for your focuser

# In flat field scripts  
TARGET_BRIGHTNESS = 20    # RGB flats
TARGET_BRIGHTNESS = 500   # Narrowband flats
```

### INDI Device Names
Verify your device names match those in the scripts:
- `"ToupTek AAF 2"` - Auto-focuser
- `"RBF Excalibur"` - Dust cap/flat panel  
- `"LX200 OnStep"` - Telescope mount

### Camera Temperature
Modify temperature settings in the EKOS sequence files:
```xml
<Temperature force='true'>-5</Temperature>
```

## 🏃‍♂️ Quick Start Example

Complete workflow for an RGB imaging session:

```bash
# 1. Start INDI server
indiserver indi_lx200_OnStep indi_simulator_ccd indi_touptek_aaf indi_excalibur &

# 2. Initialize session
python3 startup.py

# 3. Take flat fields
python3 start_flat_RGB.py
# Load and run flats_RGB.esq in EKOS

# 4. Begin light frame capture  
# Load and run lights_120s_RGB.esq in EKOS

# 5. End session
python3 shutdown.py
```

## EKOS Sequence Configuration

All sequence files are configured for:
- **Format**: RAW 16-bit FITS
- **Binning**: 1x1 (full resolution)
- **Frame Size**: 4128 x 2808 pixels
- **Temperature**: -5°C (forced)
- **Auto-guiding**: Disabled (enable in EKOS if needed)

### Exposure Times by Filter Type
- **RGB**: 120 seconds
- **Ha/OIII**: 300 seconds  
- **Flats**: 3 seconds (all filters)

## Safety Notice

**WARNING**: This software controls expensive astronomical equipment including motorized mounts, focusers, and cameras. Always:
- Test thoroughly with simulators before using real hardware
- Supervise automated operations, especially during initial setup
- Verify equipment limits and safety parameters
- Have emergency stop procedures ready

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Disclaimer**: This software is provided "AS IS" without warranty of any kind, express or implied. The authors are not responsible for any damage to equipment, data loss, or injury that may result from using this software. Use at your own risk and always test thoroughly before unattended operation.

### Third-Party Dependencies
- Hardware manufacturer terms and conditions apply to respective equipment
- INDI driver licenses apply to their respective components  
- KStars/EKOS: GPL v2+ license

## 🔗 Resources

- [KStars/EKOS Documentation](https://docs.kde.org/trunk5/en/kstars/kstars/)
- [INDI Library](https://indilib.org/)  
- [PyINDI Documentation](https://github.com/indilib/pyindi-client)
- [OnStep Telescope Controller](https://onstep.groups.io/)

---

*Clear skies! 🌌*
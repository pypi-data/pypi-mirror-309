# Frigate Event Handler

[![GitHub Release][releases-shield]][releases]
[![Python Versions][py-versions-shield]][py-versions]
![Project Maintenance][maintenance-shield]
[![License][license-shield]](LICENSE)
![Made with Love in Norway][madewithlove-shield]


A tool that listens to Frigate events and generates AI-powered descriptions of detected events using vision and language models.


## Features

- Connects to Frigate via MQTT to receive real-time events
- Processes event video clips using AI vision models
- Generates natural language descriptions of events
- Supports multiple cameras with camera-specific configurations
- Configurable frame processing (resizing, similarity detection, grid layout)
- Customizable prompts for different camera contexts

## Installation

```bash
pip install frigate-event-handler
```

## Usage

```bash
frigate-event-handler -c config.yml
```

### Command Line Options

```
usage: frigate-event-handler [-h] [-V] [-v] [--debug] [-c CONFIG]

Frigate event handler.

options:
  -h, --help            show this help message and exit
  -V, --version         show program's version number and exit
  -v, --verbose         Logging verbosity level
  --debug               Enable debug mode
  --debug-dir DEBUG_DIR
                        Directory to output debug files to.
  -c CONFIG, --config CONFIG
                        Configuration file
```

## Configuration

The tool uses a YAML configuration file to specify connection details and behavior. Here's a minimal configuration example:

```yaml
mqtt:
  host: localhost
  port: 1883
  topic: frigate/events

frigate:
  base_url: http://localhost:5000/api

vision_agent:
  api_key: your-llm-api-key
  vision_prompt: |
    Describe what you see in these surveillance camera frames.
  refine_prompt: |
    Rewrite this surveillance event description for a notification.
```

See [reference config](config.dist.yaml) for a complete configuration file with all available options and their descriptions.

### Camera-Specific Configuration

You can override global vision agent settings for specific cameras:

```yaml
vision_agent:
  # Global settings here
  cameras:
    front_door:
      prompt_context: |
        This camera faces the front door entrance.
    backyard:
      prompt_context: |
        This camera overlooks the backyard area.
```

## How It Works

1. The tool subscribes to Frigate's MQTT events
2. When an event is received, it:
    - Downloads the event video clip from Frigate
    - Extracts frames from the video
    - Processes frames (resize, similarity detection, etc.)
    - Sends frames to the vision model for analysis
    - Refines the description using a language model
3. The resulting description is then posted back to frigate

## Frame Processing Options

### Frame Similarity Detection

The tool can remove similar frames before sending them to the vision model:

```yaml
vision_agent:
  remove_similar_frames: true
  hashing_max_frames: 200
  hash_size: 12  # Lower = more aggressive similarity matching
```

### Grid Layout

Frames can be arranged in a grid:

```yaml
vision_agent:
  stack_grid: true
  stack_grid_size: [3, 3]  # 3x3 grid
```

### Frame Resizing

Control frame dimensions sent to the vision model:

```yaml
vision_agent:
  resize_video: [640, 360]  # [width, height]
```

## Debug Mode

Enable debug mode to save processed frames and API responses:

```bash
frigate-event-handler --debug -c config.yml
```

Debug files will be saved to `./debug` by default, or to a custom directory specified with the `--debug-dir` option.

Debug mode and debug directory can also be set in the configuration file.

## Requirements

- Python 3.12+
- MQTT broker
- Frigate instance
- Access to an LLM API (OpenAI compatible)

[license-shield]: https://img.shields.io/github/license/bendikrb/frigate-event-handler.svg
[license]: https://github.com/bendikrb/frigate-event-handler/blob/main/LICENSE
[releases-shield]: https://img.shields.io/pypi/v/frigate-event-handler
[releases]: https://github.com/bendikrb/frigate-event-handler/releases
[maintenance-shield]: https://img.shields.io/maintenance/yes/2024.svg
[py-versions-shield]: https://img.shields.io/pypi/pyversions/frigate-event-handler
[py-versions]: https://pypi.org/project/frigate-event-handler/
[madewithlove-shield]: https://madewithlove.now.sh/no?heart=true&colorB=%233584e4

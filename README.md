# blender-web-server

## Overview
`blender-web-server` is designed to integrate the powerful capabilities of Blender with web-based applications, enabling Blender to be accessed and controlled via a web server. This project is particularly useful for those looking to integrate Blender into web-based 3D modeling and rendering workflows. See a live implementation at [polygona.io](https://polygona.io).

Built using FastAPI, the `blender-web-server` is containerized for ease of deployment, utilizing Docker for consistent and scalable environments. For file storage and management, the project is configured to work with DigitalOcean Spaces.

## Getting Started

### Prerequisites
- Python 3.10 and `pip` (Check with `python --version` and `pip --version`)
- Docker

### Local Setup
1. **Prepare Virtual Environment**:
   - Install `virtualenv` if not already available: `pip install virtualenv`

2. **Environment Configuration**:
   - Duplicate the environment template: `cp ./app/.env-example ./app/.env`
   - Edit `./app/.env` to include the necessary environment variables.

3. **Running the Application**:
   - Execute the development script: `./dev.sh`

The application is now accessible at `http://localhost:8080`

### Docker Deployment

#### Building and Running with Docker
To build and run `blender-web-server` within a Docker container, use the following commands:

```bash
docker build -t blender-container .
docker run -it --rm -p 8080:8080 blender-container
```

This will create a Docker image named `blender-container` and run it, making the application accessible at `http://localhost:8080`.

## Contributing
We welcome contributions to `blender-web-server`! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details on how to submit pull requests, and expectations regarding code contributions.


## Support
If you find this project valuable or if it helps you in your projects, consider sponsoring it through GitHub Sponsors! Your support is essential to maintain and develop the project further.

[SPONSOR ME](https://github.com/sponsors/leota)

## License
This project is licensed under the GNU General Public License - see the [LICENSE](LICENSE.md) file for details.

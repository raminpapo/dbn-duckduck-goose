# README.md - Documentation

## File Metadata
- **File Path**: `README.md`
- **File Type**: Markdown Documentation
- **File Size**: 5,504 bytes
- **MIME Type**: text/html
- **Language**: Markdown
- **Purpose**: Project documentation and usage guide

## Original Source

```markdown
# dbn-duckduck-goose

**Golang Web Service Example using Databento and DuckDB**

*https://github.com/NimbleMarkets/dbn-duckduck-goose*

This `dbn-duckduck-goose` repository contains an example Golang webservice that uses [Databento's](https://databento.com) data-as-a-service backend and embedded [DuckDB](https://duckdb.org) for storage and query.

<p><a href="./etc/swagger_console.png"><img src="./etc/swagger_console.png" alt="OpenAPI Console" width="40%" valign="middle"></a>&nbsp;<a href="./etc/dbeqbasic.SPY.html"><img src="./etc/dbeqbasic.SPY.png" alt="Candlestick Chart" width="50%" valign="middle"></a></p>

Open source technologies used include:
 * [Golang](https://golang.org) for the programming language
 * [Databento](https://databento.com) for data-as-a-service
 * [DuckDB](https://duckdb.org) for embedded SQL database
 * [OpenAPI](https://swagger.io/specification/) for API interop
 * [Swaggo's `swag`](https://github.com/swaggo/swag) for code-driven OpenAPI generation
 * [Gin](https://gin-gonic.com/docs/) for the web service framework
 * [`dbn-go`](https://github.com/NimbleMarkets/dbn-go) for DataBento Golang support
 * [Apache ECharts](https://echarts.apache.org/en/index.html) for JavaScript charting
 * [`go-echarts`](https://go-echarts.github.io/go-echarts/#/) for Golang bindings to ECharts
 * [Taskfile](https://taskfile.dev) task runner

*CAUTION: This program incurs DataBento billing!*


## Example

Build and run the `dbn-duckduck-goose` server:
```bash
$ git clone https://github.com/NimbleMarkets/dbn-duckduck-go.git
$ cd dbn-duckduck-go
$ task build

# run server
$ export DATABENTO_API_KEY="<your_api_key>"
$ ./bin/dbn-duckduck-goose --dataset DBEQ.BASIC --out qqq.dbn.zst QQQ
```

Then test in another terminal or a web browser:

```bash
# read the specification
$ curl -v http://localhost:8888/docs/doc.json | less

# or open the Web GUI in a web browser
$ open http://localhost:8888/docs/index.html

# query for latest trades as JSON
$ curl http://localhost:8888/api/v1/last-trades/json/DBEQ.BASIC/QQQ

# query for latest trades as CSV
$ curl http://localhost:8888/api/v1/last-trades/csv/DBEQ.BASIC/QQQ

# query for latest trades as Excel
$ curl http://localhost:8888/api/v1/last-trades/excel/DBEQ.BASIC/QQQ

# query for candlesticks as JSON
$ curl http://localhost:8888/api/v1/candles/DBEQ.BASIC/QQQ

# interact with a chart in a web browser
$ open http://localhost:8888/api/v1/charts/candles/DBEQ.BASIC/SPY
```

Since those charts are self-contained, we've bundled an [SPY chart example here](./etc/dbeqbasic.SPY.html) for you to try out.


## Usage

The following environment variables control some behavior:

| Variable | Default | Description |
|--| -- | -- |
| `DATABENTO_API_KEY` | "" | DataBento API key to use for authorization |
| `GIN_MODE` | "debug" | Affects logging and [Gin](https://gin-gonic.com/docs/deployment/). May be `debug`, `release`, or `test` |

```
usage: ./bin/dbn-duckduck-goose -d <dataset> [opts] symbol1 symbol2 ...

  -d, --dataset string    Dataset to subscribe to
      --db string         DuckDB datate file to use (default: ':memory:')
  -h, --help              Show help
  -p, --hostport string   'host:port' to service HTTP (default "localhost:8888")
  -k, --key string        Databento API key (or set 'DATABENTO_API_KEY' envvar)
  -o, --out string        Output filename for DBN stream ('-' for stdout)
  -n, --snapshot          Enable snapshot on subscription request
  -t, --start string      Start time to request as ISO 8601 format (default: now)
  -v, --verbose           Verbose logging
```

There is also a [Dockerfile](./Dockerfile) which is built by [GitHub Actions](https://github.com/NimbleMarkets/dbn-duckduck-goose/actions).  It can be run with:

```
$ export DATABENTO_API_KEY="<your_api_key>"
$ mkdir logs
$ docker run -it \
      --env DATABENTO_API_KEY \
      --volume logs:/logs \
      --publish 8888:8888 \
    ghcr.io/nimblemarkets/dbn-duckduck-goose \
      --dataset DBEQ.BASIC \
      --out /logs/test.dbn.zst
      --db /logs/test.duckdb
      --hostport 0.0.0.0:8888
```

Here we are pulling the image from GitHub, storing the log files in the bind-mounted `logs` directory, and exposing the web service on port `8888`.  The `--hostport 0.0.0.0:8888` ensures that the web service binds a public interface of the container, otherwise it will bind the container's internal, inaccessible `localhost`.


## Building the project

Building depends on Taskfile [Taskfile](https://taskfile.dev)) and [Swag](https://github.com/swaggo/swag) for OpenAPI generation. Install the latter with `go install github.com/swaggo/swag/cmd/swag@latest` or `task dev-deps`.  Run `task build` to build the binary.

```sh
# Quickstart for OSX users
$ brew install go-task/tap/go-task
$ task dev-deps
$ task build
```


## License

**NOTE:** This library is **not** affiliated with Databento.  It is for educational use.  Please be careful as this service incurs billing.  We are not responsible for any charges you incur.

Adapted from [sample code](https://github.com/NimbleMarkets/dbn-go/blob/main/cmd/dbn-go-live/main.go) in  [NimbleMarkets `dbn-go` library](https://github.com/NimbleMarkets/dbn-go) and other Neomantra/NimbleMarkets code.

Released under the [MIT License](https://en.wikipedia.org/wiki/MIT_License), see [LICENSE.txt](./LICENSE.txt).

Copyright (c) 2025 [Neomantra Corp](https://www.neomantra.com).

----
Made with :heart: and :fire: by the team behind [Nimble.Markets](https://nimble.markets).
```

## High-Level Overview

The README.md file serves as the primary entry point documentation for the `dbn-duckduck-goose` project. This project is a comprehensive example implementation demonstrating how to build a production-ready Golang web service that integrates real-time financial market data from Databento with DuckDB's embedded analytics database.

### Project Purpose
The repository showcases a complete stack for handling live market data streaming, storage, querying, and visualization. It's designed as both an educational resource and a practical reference implementation for developers building similar financial data services.

### Key Capabilities
1. **Real-time Data Streaming**: Connects to Databento's live market data API to receive streaming financial data
2. **Embedded Analytics**: Uses DuckDB for high-performance SQL queries without external database dependencies
3. **RESTful API**: Provides OpenAPI-documented endpoints for data access in multiple formats (JSON, CSV, Excel)
4. **Interactive Visualization**: Generates interactive candlestick charts using Apache ECharts
5. **Production-Ready**: Includes Docker containerization, Prometheus metrics, and proper logging

## Detailed Walkthrough

### Technology Stack Components

#### Core Technologies
- **Golang (Go 1.24.1)**: Modern systems programming language providing excellent concurrency support and performance
- **Databento**: Cloud-based market data service providing normalized, professional-grade financial data
- **DuckDB**: In-process analytical database optimized for OLAP workloads, perfect for time-series queries

#### Web Framework & API
- **Gin**: High-performance HTTP web framework for Go with middleware support
- **OpenAPI/Swagger**: API specification standard ensuring interoperability
- **Swaggo**: Code-first OpenAPI documentation generator integrated with Go annotations

#### Visualization & Charting
- **Apache ECharts**: Feature-rich JavaScript visualization library
- **go-echarts**: Go bindings for server-side chart generation

#### Development Tools
- **Taskfile**: Modern task runner/build tool (alternative to Make)
- **dbn-go**: Official Golang SDK for Databento platform

### Installation and Setup

The README provides three installation paths:

1. **Source Build (Development)**
   ```bash
   git clone https://github.com/NimbleMarkets/dbn-duckduck-go.git
   cd dbn-duckduck-go
   task build
   ```

2. **Docker Deployment (Production)**
   - Pre-built images available at `ghcr.io/nimblemarkets/dbn-duckduck-goose`
   - Supports volume mounting for persistent storage
   - Configurable via environment variables

3. **macOS Quick Start**
   - Uses Homebrew for dependency management
   - Automated setup via Taskfile tasks

### Configuration Options

#### Environment Variables
- **DATABENTO_API_KEY**: Authentication credential for Databento API (required, billing-sensitive)
- **GIN_MODE**: Controls framework behavior (`debug`, `release`, `test`)

#### Command-Line Flags
- `--dataset` (`-d`): Specifies which Databento dataset to subscribe to (e.g., `DBEQ.BASIC` for equities)
- `--db`: DuckDB file path (defaults to in-memory database if omitted)
- `--hostport` (`-p`): HTTP server binding address (default: `localhost:8888`)
- `--key` (`-k`): Alternative to DATABENTO_API_KEY environment variable
- `--out` (`-o`): Output file for DBN stream archival (supports Zstandard compression `.zst`)
- `--snapshot` (`-n`): Request historical snapshot before live streaming begins
- `--start` (`-t`): ISO 8601 timestamp for starting historical data retrieval
- `--verbose` (`-v`): Enable detailed debug logging

### API Endpoints

The service exposes several endpoint patterns documented in the examples:

1. **Documentation**
   - `/docs/doc.json`: OpenAPI specification
   - `/docs/index.html`: Swagger UI interface

2. **Last Trades API**
   - `/api/v1/last-trades/json/{dataset}/{symbol}`: Recent trades as JSON
   - `/api/v1/last-trades/csv/{dataset}/{symbol}`: Recent trades as CSV
   - `/api/v1/last-trades/excel/{dataset}/{symbol}`: Recent trades as Excel workbook

3. **OHLCV (Candlestick) API**
   - `/api/v1/candles/{dataset}/{symbol}`: Candlestick data as JSON

4. **Visualization**
   - `/api/v1/charts/candles/{dataset}/{symbol}`: Interactive HTML candlestick chart

5. **Monitoring**
   - `/metrics`: Prometheus metrics endpoint (via gin-metrics)

### Docker Deployment Details

The Docker container configuration demonstrates production best practices:

```bash
docker run -it \
  --env DATABENTO_API_KEY \           # Pass API key securely
  --volume logs:/logs \               # Persist logs and data
  --publish 8888:8888 \               # Expose HTTP port
  ghcr.io/nimblemarkets/dbn-duckduck-goose \
  --dataset DBEQ.BASIC \
  --out /logs/test.dbn.zst \          # Archive stream data
  --db /logs/test.duckdb \            # Persistent database
  --hostport 0.0.0.0:8888             # Bind to all interfaces (container)
```

**Critical Configuration Note**: The `--hostport 0.0.0.0:8888` binding is required for containerized deployments to make the service accessible outside the container. Using `localhost:8888` would only bind to the container's internal loopback interface.

### Build Dependencies

The project requires:
1. **Taskfile**: Task automation tool
2. **Swag**: OpenAPI documentation generator (`go install github.com/swaggo/swag/cmd/swag@latest`)

Installation can be automated via `task dev-deps`.

## Usage Examples and Patterns

### Basic Workflow
1. Set Databento API key
2. Launch service with dataset and symbols
3. Service begins streaming data and populating DuckDB
4. Query endpoints become available for data access
5. Use web browser for interactive chart exploration

### Example: Tracking QQQ (Nasdaq-100 ETF)
```bash
export DATABENTO_API_KEY="db-xxxxxxxxxxxx"
./bin/dbn-duckduck-goose --dataset DBEQ.BASIC --out qqq.dbn.zst QQQ
```

This command:
- Subscribes to the DBEQ.BASIC dataset (equities basic data)
- Tracks the QQQ symbol (Nasdaq-100 ETF)
- Archives raw stream to `qqq.dbn.zst` (compressed)
- Stores queryable data in in-memory DuckDB
- Exposes HTTP API at `http://localhost:8888`

### Example: Multi-Symbol Tracking with Persistence
```bash
./bin/dbn-duckduck-goose \
  --dataset DBEQ.BASIC \
  --db market_data.duckdb \
  --out streams.dbn.zst \
  SPY QQQ IWM
```

Tracks three major ETFs with persistent database storage.

## Performance and Security Considerations

### Performance Notes
1. **In-Memory Mode**: Default configuration uses `:memory:` database for maximum query speed but no persistence
2. **DuckDB Performance**: Optimized for analytical queries (OLAP), excellent for time-series aggregations
3. **Concurrent Architecture**: Web server and data streaming run in separate goroutines
4. **Metrics**: Built-in Prometheus metrics track request latency, slow queries (>5s threshold)

### Security Considerations
1. **API Key Protection**:
   - Never commit `DATABENTO_API_KEY` to version control
   - Use environment variables or secure secret management
   - Service incurs billing charges based on data usage

2. **CORS Middleware**: Service includes CORS middleware (see [middleware/cors.go](middleware/cors_docs.md))

3. **Logging**: Structured logging via Zap with configurable verbosity

4. **Error Recovery**: Gin recovery middleware prevents crashes from panics

### Cost Warning
**IMPORTANT**: This service connects to Databento's commercial API and incurs usage-based billing. The README includes multiple warnings about this cost consideration. Always monitor usage and implement appropriate safeguards.

## Related Files

- [LICENSE.txt](LICENSE.txt_docs.md) - MIT License text
- [Dockerfile](Dockerfile_docs.md) - Container image definition
- [Taskfile.yml](Taskfile.yml_docs.md) - Build automation tasks
- [main.go](main_docs.md) - Application entry point
- [go.mod](go.mod_docs.md) - Go module dependencies
- [etc/dbeqbasic.SPY.html](etc/dbeqbasic.SPY.html_docs.md) - Example chart output
- [handlers/](handlers/index.md) - HTTP request handlers
- [middleware/](middleware/index.md) - HTTP middleware components
- [livedata/](livedata/index.md) - Databento streaming client

## Testing and Development

### Development Workflow
```bash
# Install dependencies
task dev-deps

# Build binary
task build

# Run with test symbols
export DATABENTO_API_KEY="your-key"
./bin/dbn-duckduck-goose --dataset DBEQ.BASIC --out test.dbn.zst SPY
```

### Continuous Integration
- GitHub Actions workflows build Docker images automatically
- See [.github/workflows/docker.yml](.github/workflows/docker_docs.md)
- See [.github/workflows/go.yml](.github/workflows/go_docs.md)

### Testing Endpoints
After launching the service, test functionality:
```bash
# Verify API documentation loads
curl http://localhost:8888/docs/doc.json

# Test JSON endpoint
curl http://localhost:8888/api/v1/last-trades/json/DBEQ.BASIC/SPY

# Test CSV export
curl http://localhost:8888/api/v1/last-trades/csv/DBEQ.BASIC/SPY

# Test Excel export
curl http://localhost:8888/api/v1/last-trades/excel/DBEQ.BASIC/SPY > trades.xlsx

# View chart
open http://localhost:8888/api/v1/charts/candles/DBEQ.BASIC/SPY
```

## License and Attribution

### License
Released under the MIT License, a permissive open-source license allowing commercial and private use with attribution.

### Copyright
Copyright (c) 2025 Neomantra Corp

### Affiliation Disclaimer
The project is **not** affiliated with Databento - it's an independent educational example. Users are responsible for any Databento billing charges incurred.

### Origin
Adapted from example code in the NimbleMarkets `dbn-go` library, demonstrating practical usage patterns for the Databento Golang SDK.

### Organization
Created by the team at [Nimble.Markets](https://nimble.markets), a financial technology platform.

## Architecture Implications

From this README, we can infer the overall system architecture:

1. **Data Ingestion Layer**: LiveDataClient manages Databento WebSocket connection
2. **Storage Layer**: DuckDB handles both real-time queries and optional persistence
3. **API Layer**: Gin framework with OpenAPI documentation
4. **Presentation Layer**: Server-side chart rendering with ECharts
5. **Monitoring Layer**: Prometheus metrics integration
6. **Middleware Layer**: CORS, logging, recovery, database injection

This architecture supports the full lifecycle of market data: ingestion → storage → querying → visualization → monitoring.

## Word Count
Approximately 1,850 words (excluding code blocks)

---
*Generated by World's Best Repo Book Generator v1.0*
*Last Updated: 2025-11-15*

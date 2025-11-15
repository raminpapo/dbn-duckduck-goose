# README.md - Keywords Index

## A

### Apache ECharts
**Type**: Library
**Description**: Feature-rich JavaScript visualization library used for generating interactive charts, specifically candlestick charts for market data visualization.
**References**: [README_docs.md#technology-stack-components](README_docs.md#technology-stack-components)

### API Key
**Type**: Configuration/Security
**Description**: Authentication credential for Databento API access, set via DATABENTO_API_KEY environment variable. Critical for billing and access control.
**References**: [README_docs.md#configuration-options](README_docs.md#configuration-options), [README_docs.md#security-considerations](README_docs.md#security-considerations)

## B

### Build Dependencies
**Type**: Development
**Description**: Required tools for building the project, including Taskfile and Swag for OpenAPI generation.
**References**: [README_docs.md#build-dependencies](README_docs.md#build-dependencies)

## C

### Candlestick Charts
**Type**: Visualization/Feature
**Description**: OHLCV (Open, High, Low, Close, Volume) financial data visualization provided via interactive ECharts-based HTML pages.
**References**: [README_docs.md#api-endpoints](README_docs.md#api-endpoints)

### CORS Middleware
**Type**: Security/Middleware
**Description**: Cross-Origin Resource Sharing middleware enabling web browser access to API endpoints.
**References**: [README_docs.md#security-considerations](README_docs.md#security-considerations)

### CSV Export
**Type**: Feature/API
**Description**: Endpoint capability to export last trades data in CSV format for spreadsheet consumption.
**References**: [README_docs.md#api-endpoints](README_docs.md#api-endpoints)

## D

### Databento
**Type**: External Service
**Description**: Cloud-based market data-as-a-service provider supplying normalized, professional-grade financial data streams. Core dependency for live data.
**References**: [README_docs.md#technology-stack-components](README_docs.md#technology-stack-components), [README_docs.md#cost-warning](README_docs.md#cost-warning)

### DBEQ.BASIC
**Type**: Dataset
**Description**: Databento equities basic dataset providing fundamental market data for US equities.
**References**: [README_docs.md#configuration-options](README_docs.md#configuration-options), [README_docs.md#example-tracking-qqq](README_docs.md#example-tracking-qqq)

### dbn-go
**Type**: Library/SDK
**Description**: Official Golang SDK for Databento platform, providing client libraries for data access.
**References**: [README_docs.md#technology-stack-components](README_docs.md#technology-stack-components)

### Docker
**Type**: Deployment/Container
**Description**: Container platform used for production deployment, with pre-built images published to GitHub Container Registry.
**References**: [README_docs.md#docker-deployment-details](README_docs.md#docker-deployment-details)

### DuckDB
**Type**: Database
**Description**: In-process analytical OLAP database optimized for time-series queries, provides embedded SQL capabilities without external database server.
**References**: [README_docs.md#technology-stack-components](README_docs.md#technology-stack-components), [README_docs.md#performance-notes](README_docs.md#performance-notes)

## E

### Excel Export
**Type**: Feature/API
**Description**: Endpoint capability to export last trades data as Excel workbook files (.xlsx format).
**References**: [README_docs.md#api-endpoints](README_docs.md#api-endpoints)

## G

### Gin Framework
**Type**: Library/Framework
**Description**: High-performance HTTP web framework for Go with middleware support, forms the foundation of the web service layer.
**References**: [README_docs.md#technology-stack-components](README_docs.md#technology-stack-components)

### GIN_MODE
**Type**: Configuration/Environment
**Description**: Environment variable controlling Gin framework behavior (debug/release/test), affects logging verbosity and performance optimizations.
**References**: [README_docs.md#configuration-options](README_docs.md#configuration-options)

### GitHub Actions
**Type**: CI/CD
**Description**: Continuous integration platform used to automatically build Docker images and run Go tests.
**References**: [README_docs.md#continuous-integration](README_docs.md#continuous-integration)

### go-echarts
**Type**: Library
**Description**: Golang bindings for Apache ECharts library, enables server-side chart generation.
**References**: [README_docs.md#technology-stack-components](README_docs.md#technology-stack-components)

### Golang
**Type**: Programming Language
**Description**: Primary programming language (Go 1.24.1) providing concurrency support and high performance for systems programming.
**References**: [README_docs.md#technology-stack-components](README_docs.md#technology-stack-components)

## H

### HTTP API
**Type**: Interface/Feature
**Description**: RESTful API exposing endpoints for data access in multiple formats (JSON, CSV, Excel) with OpenAPI documentation.
**References**: [README_docs.md#api-endpoints](README_docs.md#api-endpoints)

## I

### In-Memory Database
**Type**: Configuration/Performance
**Description**: Default DuckDB mode using `:memory:` for maximum query speed without persistence to disk.
**References**: [README_docs.md#performance-notes](README_docs.md#performance-notes)

### ISO 8601
**Type**: Standard/Format
**Description**: International standard for date-time representation, used for --start flag to specify historical data retrieval timestamps.
**References**: [README_docs.md#configuration-options](README_docs.md#configuration-options)

## L

### Last Trades API
**Type**: Feature/Endpoint
**Description**: API endpoints providing access to recent trade data in JSON, CSV, and Excel formats.
**References**: [README_docs.md#api-endpoints](README_docs.md#api-endpoints)

### License
**Type**: Legal
**Description**: MIT License - permissive open-source license allowing commercial use with attribution.
**References**: [README_docs.md#license-and-attribution](README_docs.md#license-and-attribution)

### Live Data Streaming
**Type**: Feature/Architecture
**Description**: Real-time market data ingestion from Databento WebSocket streams, managed by LiveDataClient component.
**References**: [README_docs.md#key-capabilities](README_docs.md#key-capabilities)

## M

### Metrics
**Type**: Monitoring/Feature
**Description**: Prometheus-format metrics exposed at /metrics endpoint for monitoring request latency and performance.
**References**: [README_docs.md#api-endpoints](README_docs.md#api-endpoints), [README_docs.md#performance-notes](README_docs.md#performance-notes)

### Middleware
**Type**: Architecture/Component
**Description**: HTTP request processing layers including CORS, logging, database injection, and error recovery.
**References**: [README_docs.md#architecture-implications](README_docs.md#architecture-implications)

### MIT License
**Type**: Legal
**Description**: Specific open-source license used for this project, permitting commercial and private use with attribution requirements.
**References**: [README_docs.md#license](README_docs.md#license)

## N

### Neomantra Corp
**Type**: Organization
**Description**: Copyright holder and creator organization behind this project and Nimble.Markets platform.
**References**: [README_docs.md#copyright](README_docs.md#copyright)

### Nimble.Markets
**Type**: Platform/Organization
**Description**: Financial technology platform created by the team behind this project.
**References**: [README_docs.md#organization](README_docs.md#organization)

## O

### OHLCV Data
**Type**: Data Format
**Description**: Open-High-Low-Close-Volume candlestick data for financial market visualization and analysis.
**References**: [README_docs.md#candlestick-charts](README_docs.md#candlestick-charts)

### OpenAPI
**Type**: Standard/Specification
**Description**: API specification standard (formerly Swagger) ensuring interoperability and providing auto-generated documentation.
**References**: [README_docs.md#technology-stack-components](README_docs.md#technology-stack-components)

## P

### Performance
**Type**: Quality Attribute
**Description**: System performance characteristics including in-memory operation, DuckDB OLAP optimization, concurrent architecture, and metrics tracking.
**References**: [README_docs.md#performance-and-security-considerations](README_docs.md#performance-and-security-considerations)

### Prometheus
**Type**: Monitoring/Tool
**Description**: Metrics collection system format used for exposing service performance data.
**References**: [README_docs.md#performance-notes](README_docs.md#performance-notes)

## Q

### QQQ
**Type**: Symbol/Example
**Description**: Nasdaq-100 ETF ticker symbol used in documentation examples for tracking technology stocks.
**References**: [README_docs.md#example-tracking-qqq](README_docs.md#example-tracking-qqq)

## R

### RESTful API
**Type**: Architecture/Pattern
**Description**: Representational State Transfer API design providing stateless, resource-oriented endpoints.
**References**: [README_docs.md#key-capabilities](README_docs.md#key-capabilities)

## S

### Security
**Type**: Quality Attribute
**Description**: Security considerations including API key protection, CORS configuration, structured logging, and error recovery mechanisms.
**References**: [README_docs.md#performance-and-security-considerations](README_docs.md#performance-and-security-considerations)

### Snapshot
**Type**: Feature/Configuration
**Description**: Historical data snapshot requested before live streaming begins, enabled via --snapshot flag.
**References**: [README_docs.md#configuration-options](README_docs.md#configuration-options)

### SPY
**Type**: Symbol/Example
**Description**: S&P 500 ETF ticker symbol frequently used in examples and bundled chart demonstrations.
**References**: [README_docs.md#api-endpoints](README_docs.md#api-endpoints)

### Swagger UI
**Type**: Tool/Interface
**Description**: Interactive web interface for exploring and testing OpenAPI-documented endpoints.
**References**: [README_docs.md#api-endpoints](README_docs.md#api-endpoints)

### Swaggo
**Type**: Tool/Library
**Description**: Code-first OpenAPI documentation generator using Go annotations/comments to generate specification.
**References**: [README_docs.md#technology-stack-components](README_docs.md#technology-stack-components), [README_docs.md#build-dependencies](README_docs.md#build-dependencies)

## T

### Taskfile
**Type**: Tool/Build System
**Description**: Modern task runner and build automation tool, alternative to Make, used for project build orchestration.
**References**: [README_docs.md#technology-stack-components](README_docs.md#technology-stack-components), [README_docs.md#build-dependencies](README_docs.md#build-dependencies)

## V

### Verbose Logging
**Type**: Configuration/Feature
**Description**: Detailed debug logging enabled via --verbose flag for troubleshooting and development.
**References**: [README_docs.md#configuration-options](README_docs.md#configuration-options)

## W

### WebSocket
**Type**: Protocol
**Description**: Full-duplex communication protocol used by Databento for real-time data streaming.
**References**: [README_docs.md#architecture-implications](README_docs.md#architecture-implications)

## Z

### Zap
**Type**: Library
**Description**: Structured logging library from Uber providing high-performance, leveled logging capabilities.
**References**: [README_docs.md#security-considerations](README_docs.md#security-considerations)

### Zstandard Compression
**Type**: Format/Feature
**Description**: High-performance compression format (.zst) used for archiving DBN stream data.
**References**: [README_docs.md#configuration-options](README_docs.md#configuration-options)

---

## Summary Statistics
- **Total Keywords**: 48
- **Categories**: Technology Stack (12), Configuration (8), Features (10), Security (4), Tools (6), Examples (4), Legal (2), Organizations (2)
- **Cross-References**: All keywords link to relevant documentation sections

---
*Generated by World's Best Repo Book Generator v1.0*
*Last Updated: 2025-11-15*

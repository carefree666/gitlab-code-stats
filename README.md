# 🧮 GitLab Code Stats / GitLab 代码统计工具

[English](#english-version) | [中文](#中文说明)

---

## English Version

### Overview
`gitlab-code-stats` is a Python-based tool for collecting GitLab user commit statistics and exporting results to CSV. It also provides a Web API for querying statistics and downloading CSV reports.

### Features
- Fetch user commit data from GitLab REST API  
- Date-range filtering  
- Maximum lines per commit (`max_lines_per_commit`)  
- Export results to CSV  
- Configurable user list  
- CLI and Web API support  
- Docker support for multi-arch images  
- One-command packaging via Makefile  

### CLI Usage
Run command-line statistics:
```bash
make run
```
Results will be saved as CSV (default `gitlab_code_stats.csv`, configurable in `config.json`).

### Web API Usage
Start the web service:
```bash
make web
```
Open Swagger documentation:
```
http://localhost:8000/docs
```
Example POST request to `/stats`:
```json
{
  "start_date": "2025-10-01T00:00:00Z",
  "end_date": "2025-10-31T23:59:59Z",
  "users": ["zhangsan"]
}
```
Example CSV response fields:
```
Username, Name, CommitCount, TotalLines, Additions, Deletions
```

### Docker Usage
Build and run Docker image:
```bash
make docker-build
```
Or manually:
```bash
docker build -t gitlab-code-stats .
docker run -v $(pwd)/config.json:/app/config.json gitlab-code-stats
```
Supports multi-arch images for linux/amd64 and linux/arm64.

### Packaging
Create source tar.gz package:
```bash
make package
```

### Configuration
Example `config.json`:
```json
{
  "api_url": "https://gitlab.example.com/api/v4",
  "private_token": "YOUR_TOKEN_HERE",
  "start_date": "2025-10-01T00:00:00Z",
  "end_date": "2025-10-31T23:59:59Z",
  "users": ["zhangsan"],
  "output_filename": "gitlab_code_stats.csv",
  "max_lines_per_commit": 1000
}
```

---

## 中文说明

### 简介
`gitlab-code-stats` 用于统计 GitLab 用户代码提交情况，并导出 CSV 文件。支持 CLI 和 Web API 调用，同时可通过 Docker 部署。

### 功能
- 调用 GitLab API 获取用户提交数据  
- 支持时间范围过滤  
- 每个 commit 行数可限制 (`max_lines_per_commit`)  
- 导出 CSV 文件  
- 可配置用户列表  
- CLI 和 Web API 支持  
- Docker 支持（多架构镜像）  
- Makefile 支持一键运行、打包  

### CLI 使用
```bash
make run
```
生成 CSV 文件（默认 `gitlab_code_stats.csv`，可通过 `config.json` 配置）。

### Web API 使用
```bash
make web
```
Swagger 文档：
```
http://localhost:8000/docs
```
POST `/code-stats` 请求示例：
```json
{
  "start_date": "2025-10-01T00:00:00Z",
  "end_date": "2025-10-31T23:59:59Z",
  "users": ["zhangsan"]
}
```
CSV 响应字段：
```
Username, Name, CommitCount, TotalLines, Additions, Deletions
```

### Docker 使用
```bash
make docker-build
# 或者手动
docker build -t gitlab-code-stats .
docker run -v $(pwd)/config.json:/app/config.json gitlab-code-stats
```
支持多架构：`linux/amd64`, `linux/arm64`。

### 打包
创建源码 tar.gz：
```bash
make package
```

### 配置示例
```json
{
  "api_url": "https://gitlab.example.com/api/v4",
  "private_token": "YOUR_TOKEN_HERE",
  "start_date": "2025-10-01T00:00:00Z",
  "end_date": "2025-10-31T23:59:59Z",
  "users": ["zhangsan"],
  "output_filename": "gitlab_code_stats.csv",
  "max_lines_per_commit": 1000
}
```



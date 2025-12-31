# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AI Product Research is a Python application that automatically analyzes products from Product Hunt, extracts business
problem information using LLM vision capabilities, filters AI-powered products, and posts analysis to a Telegram
channel. The application runs as a scheduled service (daily at 6 AM CET).

## Technology Stack

- **Python 3.13** with uv package manager
- **LangChain** for LLM orchestration (OpenAI GPT-5 models)
- **Playwright** for web scraping and screenshots
- **Pydantic** for data validation and settings management
- **pytest** with async support for testing
- **Telegram Bot API** for posting updates

## Development Commands

### Environment Setup

```bash
# Install dependencies (uses uv package manager)
uv sync

# Install with dev dependencies
uv sync --dev
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/test_ai_product_research/test_agents/test_problem_retriever_agent.py

# Run specific test function
uv run pytest tests/test_ai_product_research/test_agents/test_problem_retriever_agent.py::TestProblemRetrieverAgent::test_retrieves_business_problems_with_high_average_score
```

### Running the Application

```bash
# Run the main application
uv run python -m ai_product_research.main

# Run in debug mode (processes yesterday's products immediately)
# Set AI_PRODUCT_RESEARCH_DEBUG=true in .env file
```

### Docker Operations

```bash
# Build Docker image
make docker-build

# Build and push to registry
make docker-build-push

# Full release (build, push, deploy)
make release
```

## Architecture

### Core Components

**Application Context (`app_context.py`)**

- Dependency injection container that initializes all services, agents, and use cases
- Created via `create_app_context()` function
- Contains LLM instances, services, agents, and settings

**Main Flow (`main.py`)**

- Scheduler that runs daily at 6 AM CET
- In debug mode, immediately processes previous day's products
- Delegates to `TelegramProductsResearchUseCase` for business logic

**Use Case Layer (`usecase/telegram_products_research_use_case.py`)**

- Orchestrates the complete workflow:
    1. Fetch Product Hunt posts from target date
    2. Scrape product websites for screenshots
    3. Use `ProblemRetrieverAgent` to analyze screenshots
    4. Use `ProductFilterAgent` to filter AI-powered products
    5. Send top 3 filtered products to Telegram channel
    6. If less than 3 pass filter, backfill with top-rated products

**Agent Layer**

- `ProblemRetrieverAgent` (`agents/problem_retriever_agent.py`):
    - Uses vision-capable LLM to extract business problem from screenshot
    - Returns structured `BusinessProblem` (primary_customer, core_job, main_pain, success_metric)

- `ProductFilterAgent` (`agents/product_filter_agent.py`):
    - Filters products based on three criteria: uses AI/LLM, solves real problems, has $10K+ MRR potential
    - Returns boolean pass/fail decision

**Service Layer**

- `ProductHuntService`: Fetches products via Product Hunt API
- `WebSiteScrapperService`: Uses Playwright to capture website screenshots
- `AnalyzedProductTelegramChannelService`: Posts formatted product analysis to Telegram

**Domain Models (`domain/`)**

- `BusinessProblem`: Primary customer, core job, main pain, success metric
- `AnalyzedProduct`: Product with extracted business problem
- `ProductHuntPost`: Product Hunt post data

### Configuration

Settings are managed via Pydantic Settings with environment variables prefixed `AI_PRODUCT_RESEARCH_`:

- `OPENAI_API_KEY`: OpenAI API key for GPT models
- `TELEGRAM_BOT_TOKEN`: Telegram bot token
- `TELEGRAM_CHANNEL_ID`: Target Telegram channel
- `PRODUCT_HUNT_DEV_TOKEN`: Product Hunt API token
- `DEBUG`: Enable debug mode (runs immediately instead of on schedule)

Configuration file: `.env` (not committed to git)

### Testing Strategy

Tests use LLM-based evaluation for agent quality:

- `BusinessProblemEvaluator`: Uses LLM as a judge to score retrieval accuracy (0.0-1.0)
- Screenshot-based test cases with expected results
- Threshold-based assertions (e.g., average score >= 0.9)
- Async test support via pytest-asyncio

## Key Design Patterns

1. **Dependency Injection**: All dependencies created in `create_app_context()` and passed explicitly
2. **Structured Outputs**: LangChain's `with_structured_output()` for type-safe LLM responses
3. **Agent Pattern**: Specialized agents (ProblemRetriever, ProductFilter) with focused responsibilities
4. **Use Case Pattern**: Business logic isolated in use case classes
5. **LLM-as-Judge**: Test evaluation using LLM to assess quality of AI outputs

## Important Notes

- The application runs continuously as a daemon, executing once daily
- Uses Playwright with Chromium for screenshot capture (requires browser installation in Docker)
- OpenAI GPT-5 models are used (gpt-5-mini and gpt-5-nano)
- Product filtering ensures only AI-powered products with market potential are surfaced
- Backfill strategy ensures 3 products are always posted, even if filter is too strict

## Scratchpad Technique (Branch Analysis)

When working on a feature branch, maintain a scratchpad file to track thoughts, progress, and decisions:

**File Location**: `.claude/branch-analysis.md`

**Purpose**:

- Document your thought process and analysis as you work
- Track progress on tasks and milestones
- Record decisions made and their rationale
- Maintain context across multiple sessions
- Keep notes about code exploration and discoveries

**Workflow**:

1. When starting work on any branch, create or update `.claude/branch-analysis.md`
2. Use it as a working scratchpad to document:
    - Initial analysis and understanding of the task
    - Code exploration findings (files examined, patterns discovered)
    - Implementation decisions and trade-offs
    - Progress updates as you complete subtasks
    - Blockers or questions that arise
    - Test results and validation outcomes
3. Update the file throughout your work session
4. Use markdown formatting for clarity

**Example Structure**:

```markdown
# Branch Analysis: [branch-name]

## Objective

[Brief description of the task/feature]

## Initial Analysis

[Your understanding after exploring the codebase]

## Progress

- [x] Task 1
- [ ] Task 2 (in progress)
- [ ] Task 3

## Decisions & Rationale

- **Decision**: [What you decided]
    - **Why**: [Reasoning]

## Notes & Discoveries

- [Observations about the codebase]
- [Patterns or conventions found]

## Blockers

- [Any issues or questions]
```

**Note**: This file is for internal use and should not be committed to the repository. Add `.claude/branch-analysis.md`
to `.gitignore` if needed.

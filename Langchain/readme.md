(eng)
# LangChain Study

> Personal study notes. Because these were written quickly, readability may be uneven. I’ll refine examples and content over time.

---

## What is LangChain?

**LangChain** is an open-source framework for quickly building **LLM-based agents and applications**.
It integrates various models (OpenAI, Anthropic, Google, etc.) and tools/databases, and lets you compose **prompts, chains, memory, and tool calls** to build reliable agents.

---

## Why study LangChain?

**Goal:** Connect multiple APIs and run AI **locally**.

* Experiment locally/in-house by swapping among different LLMs (OpenAI, Anthropic, Google, etc.) via a **pluggable interface**.
* Build a **RAG pipeline** quickly with standard components to search external knowledge (files, databases, web) and enhance answers.
* Let agents **automatically call tools** (search, code execution, DB queries, and more) to carry out complex, multi-step tasks.
* In operations, extend to **tracing/evaluation/observability** (e.g., with LangSmith) for reproducible experiments and iterative improvement.

(kor)
# LangChain 스터디

> 개인 학습용 정리 문서입니다. 빠르게 기록한 노트라 **가독성이 다소 떨어질 수 있습니다.** 필요 시 예제 코드와 내용 보완할 예정입니다.

---

## LangChain은 무엇인가

* **LangChain**은 대규모 언어 모델(LLM) 기반 **에이전트·애플리케이션**을 빠르게 만들기 위한 오픈소스 프레임워크
* 다양한 모델(OpenAI, Anthropic, Google 등)과 도구/데이터베이스를 **통합**하고, 프롬프트·체인·메모리·도구 호출을 조합해 **신뢰 가능한 에이전트**를 구성

---

## LangChain을 공부하는 이유

**목표**: 여러 API를 연동해 **로컬 환경에서 AI를 직접 구동**해 보기 위함.

* 로컬/사내 환경에서 OpenAI, Anthropic, Google 등 다양한 LLM을 **플러그형 인터페이스**로 바꿔 끼며 실험 가능
* 파일, 데이터베이스, 웹 소스 등 외부 지식을 검색해 답변을 보강하는 **RAG 파이프라인**을 표준 구성요소로 빠르게 구축
* 에이전트가 도구(검색, 코드 실행, DB 질의 등)를 **자동 호출**하도록 연결해 복잡한 작업을 단계적으로 수행
* 운영 단계에서 **트레이싱/평가/관측**(LangSmith)까지 이어 붙여 재현 가능한 실험·개선 가능

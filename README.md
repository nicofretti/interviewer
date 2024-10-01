![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)
# 🎙️ Interviewer

> A cutting-edge AI-powered interview simulation system


## 🌟 Features

-   🤖 AI-powered interviewer and candidate
-   🎯 Customizable interview questions based on field and domain
-   💾 Export interactions to a JSON file

## 🚀 Quick Start

1. Set the `ANTHROPIC_API_KEY` environment variable:

    ```sh
    set ANTHROPIC_API_KEY=your_api_key_here
    ```

2. Launch the application:

    ```sh
    python __main__.py
    ```

3. 🎉 Watch as the AI conducts multiple interview sessions and exports the interactions to JSON files!

## 💡 Example

For a Software Engineer interview focusing on System Design and Architecture, the app generates:

📄 `software_engineer_system_design_and_architecture.json`

```json
[
    {
        "role": "Interviewer",
        "message": "Describe the design of a scalable and fault-tolerant distributed system for a social media platform. Discuss the key components, their responsibilities, and how they interact to ensure high availability and performance."
    },
    {
        "role": "Candidate",
        "message": "Here's a high-level design for a scalable and fault-tolerant distributed system for a social media platform:\n\nKey components:\n1. Load Balancer: Distributes incoming requests across multiple application servers for optimal performance and fault tolerance. Uses algorithms like round-robin or least connections.\n\n2. Application Servers: Handle business logic, process requests, and generate responses. Stateless for easy scaling. Multiple servers deployed across different availability zones for high availability.\n\n3. Caching Layer: In-memory cache (like Redis) to store frequently accessed data. Reduces load on databases and improves response times. Distributed cache deployed in a cluster for scalability and fault tolerance.\n\n4. Database: Stores persistent data. Sharded and replicated for scalability and high availability. Master-slave replication for read-heavy workloads. Eventual consistency model for faster writes.\n\n5. Message Queue: Decouples components and enables asynchronous processing. Handles tasks like notifications, updates, and background jobs. Ensures reliable delivery and prevents data loss.\n\n6. Content Delivery Network (CDN): Caches static content (images, videos) closer to users. Reduces load on origin servers and improves loading speeds. Multiple edge locations worldwide for low latency.\n\nInteractions:\n- Requests hit the load balancer, which routes them to an available application server.\n- Application servers first check the cache for data. If not found, they query the database.\n- Writes are committed to the database and then updated in the cache.\n- Async tasks are published to the message queue for background processing.\n- Static content is served from the CDN, reducing load on application servers.\n\nThis design ensures high availability through redundancy, fault tolerance via multiple instances, and scalability by allowing components to scale independently based on load."
    }
    // ... more interactions
]
```

Take a look at the examples in the `examples` directory for more!

## 🛠️ Technical Details

-   **Language**: Python
-   **AI Model**: Anthropic's API
-   **Output**: JSON

```python
conduct_interview(
    interactions=15,
    field="Software Engineer",
    domain="Algorithms and Data Structures",
    filename="software_engineer_algorithms_data_structures.json",
)
```

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Happy auto-interviewing! Miaooo! 🐱
</p>

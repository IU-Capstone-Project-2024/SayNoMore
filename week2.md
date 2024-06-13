# —
title: "Week #2"
---

# **Week #2**

## **Week 2 - Choosing the Tech Stack, Designing the Architecture**

### **Tech Stack Selection**

The technology stack for **SayNoMore** will include:
1. **Backend:**
   - **Python:** Core programming language for building the application logic and integrating AI functionalities.
   - **Flask/Django:** ***(Potential future integration)*** Web frameworks for developing the backend API and managing server-side operations.
   - **LLaMA (Language Model) Library:** Utilized for natural language processing to interpret user queries and extract necessary information.
   - **PostgreSQL:** Database for storing user data, travel details, and system logs.
2. **Frontend:**
   - **Telegram Bot API:** Interface for user interaction, allowing seamless communication and engagement with the chatbot.
   - **HTML/CSS/JavaScript:** ***(Potential future integration)*** Basic frontend technologies for any web components or user interface elements required.
3. **APIs and Integrations:**
   - **Aviasales API:** For retrieving comprehensive flight and hotel data, ensuring users have access to the latest travel information.
   - **Google Maps API:** ***(Potential future integration)*** For providing location-based services and visualizing travel routes and destinations.
4. **AI and Machine Learning:**
   - **LLaMA (Language Model) Library:** Core library for developing NLP capabilities to understand and process user inputs.
   - **Scikit-learn/TensorFlow/PyTorch**: ***(Potential future integration)*** Machine learning frameworks for implementing recommendation algorithms and personalized travel suggestions.
5. **DevOps and Deployment:**
   - **Docker:** For containerizing the application to ensure consistent environments across development and production.
   - **AWS/GCP/Azure/YaCloud:** Cloud platforms for hosting the application, providing scalability, and managing storage and computing resources.
   - **CI/CD Tools:** Jenkins/GitHub Actions for automating deployment and ensuring continuous integration and delivery.

TechStack requied for the Proof of Concept:
- Python
- LLaMa
- AviaSales API, Telegram Bot API
- Docker, GitHub Actions

### **Architecture Design**
1. **Component Breakdown**:
   The **SayNoMore** project is structured into three main modules, each responsible for different aspects of the system:
   - **Module A: Request Analyzer**
     - **Purpose**: Handles the extraction and verification of user inputs.
     - **Key Components**: 
       - **RequestAnalyzer Class**: Orchestrates the overall request processing.
       - **InformationRetrieval Classes**: Extract specific travel details like destination, dates, and budget.
       - **RequestVerification Classes**: Validate the accuracy and relevancy of the extracted information.
  
   - **Module B: API Collector**
     - **Purpose**: Fetches real-time data on flights and hotels from external APIs.
     - **Key Components**:
       - **AirTicketsApi Class**: Retrieves flight information, including prices and availability.
       - **HotelApi Class**: Retrieves hotel data, including room availability and pricing.
  
   - **Module C: Telegram Bot Interface**
     - **Purpose**: Facilitates user interaction through the Telegram Bot API.
     - **Key Components**:
       - **Telegram Bot**: Acts as the main user interface, handling communication with users.
       - **Conversation Handler**: Manages the dialogue flow and collects user information.
Graphical representation and interconection of those 3 modules:
![FirstProtoUML](https://hackmd.io/_uploads/BJ5BSg7BA.png)
2. **Data Management**:
   Efficient data management is critical for the **SayNoMore** project, particularly in leveraging the Telegram system’s data organization and management capabilities. Here’s how we plan to handle data:
   - **Database**:
     - **PostgreSQL**: 
       - Centralized storage for user profiles, travel details, and system logs.
       - Selected for its scalability and robustness in managing structured data.
     - **Telegram Data Storage**:
       - Utilizes Telegram’s built-in data organization for managing user interactions and session states.
       - Ensures efficient handling and retrieval of user messages and session information.
   - **Data Storage**:
     - **User Data**: 
       - Stores user preferences, profiles, and interaction histories.
       - Integrates with Telegram's system to maintain session continuity and user state across interactions.
     - **Travel Information**:
       - Caches flight and hotel data fetched from external APIs to enhance response times.
       - Ensures up-to-date travel options are readily available for user queries.
   - **Data Flow**:
     - **Retrieval and Processing**:
       - Module B collects travel data from external APIs.
       - Module C captures user inputs via Telegram, with data processed and verified by Module A.
     - **Synchronization**:
       - Maintains consistent and synchronized data across modules and the Telegram bot interface.
       - Ensures seamless integration of user inputs and travel data, leveraging Telegram’s real-time data management.
   - **Data Security**:
     - **Encryption**:
       - Uses HTTPS/SSL to secure data transmission between users, the backend, and external APIs.
       - Utilizes Telegram’s built-in security features to protect data in transit.
     - **Authentication**:
       - Integrates Telegram’s authentication mechanisms for verifying user sessions.
   - **Backup and Recovery**:
     - **Regular Backups**:
       - Performs routine backups of PostgreSQL data to safeguard against data loss.
       - Leverages Telegram’s reliable session management to maintain continuity.
     - **Recovery Plans**:
       - Develops strategies to quickly restore operations in case of data disruptions.
   - **Logging and Monitoring**:
     - **Activity Logs**:
       - Logs user interactions and system events for auditing and troubleshooting.
       - Incorporates Telegram’s logging capabilities to track session activities.
     - **Performance Monitoring**:
       - Monitors Telegram’s performance metrics to ensure smooth data handling and user interactions.
3. **User Interface (UI) Design**:
   Currently, **SayNoMore** uses the Telegram Bot UI for user interactions, providing a straightforward and familiar way to plan travel. We also have plans to expand to web and mobile platforms for a richer user experience. 
   - **Telegram Bot Interface**:
     - **Main Interaction Platform**:
       - Utilizes Telegram’s chatbot to guide users through travel planning with a text-based interface.
       - Users can input details, get recommendations, and interact seamlessly.
     - **User-Friendly Features**:
       - Supports quick replies and interactive messages for easy navigation.
       - Integrates with Telegram’s conversation flow for smooth interactions.
     - **Session Management**:
       - Maintains continuity and context using Telegram’s session management.
       - Allows users to start, pause, and resume planning without losing progress.
   - **Future Web and Mobile Platforms**:
     - **Transition to Web and Mobile**:
       - Plans to develop a responsive web interface using React and native mobile apps for iOS and Android using frameworks like React Native or Flutter.
       - Aims to provide a more comprehensive and visually rich experience.
     - **Enhanced User Experience**:
       - The web and mobile platforms will include features like graphical travel route visualization, interactive maps, and detailed itinerary management.
       - Leverages mobile capabilities such as push notifications and location services for better user engagement.
     - **Consistency Across Platforms**:
       - Ensures a unified and seamless experience across Telegram, web, and mobile platforms.
       - Maintains consistent functionality and design principles across all interfaces.
4. **Integration and APIs**:
   * **External APIs**:
     * **Aviasales API**: Fetches real-time data on flights and hotels, ensuring users receive the most relevant and current travel options.
     * **Google Maps API** (Future): Potential integration for geolocation services and travel route visualization.
   * **Internal APIs**:
     * Ensures smooth data exchange between different modules within the system.
     * Facilitates seamless integration of the Telegram bot with backend services.

5. **Scalability and Performance**:
   - **Containerization**:
     * **Docker**: Used for packaging applications into containers, ensuring consistency across different environments.
   * **Cloud Services**:
     * **AWS/YaCoud/ VKCloud**: Chosen cloud platforms for hosting and scaling the application based on user demand.
   * **Load Balancing**:
     * Strategies to distribute traffic and maintain optimal performance under varying loads.

6. **Security and Privacy**:
   - **HTTPS/SSL/TLS**: Ensures secure data transmission between users and the system.

7. **Error Handling and Resilience**:
   * **Robust Error Handling**:
     * Strategies to manage and log errors gracefully, providing clear feedback to users and maintaining system stability.
   * **Resilience**:
     * Designs to ensure the system remains functional and responsive under various failure conditions.

8. **Deployment and DevOps**:
   * **Continuous Integration/Continuous Deployment (CI/CD)**:
     * **GitHub Actions**: Automates testing and deployment processes to ensure reliable updates and integrations.

### **Week 2 questionnaire:**

1) Tech Stack Resources: ...

2) Mentorship Support: ...

3) Exploring Alternative Resources: ...

4) Identifying Knowledge Gaps: ...

5) Engaging with the Tech Community: ...

6) Learning Objectives: ...

7) Sharing Knowledge with Peers: ...

8) Leveraging AI: ...

### **Tech Stack and Team Allocation**
| Team Member         | Role             | Responsibilities                                             |
|---------------------|------------------|--------------------------------------------------------------|
| Maxim Martyshov     | DevOps, PM, Lead | - Leading the project<br>- Managing CI/CD pipelines<br>- Maintaining GitHub repository<br>- Writing and breaking down tasks and issues<br>- Writing and overseeing reports<br>- Conceptual development<br>- Developing the Telegram bot |
| Elisei Smirnov      | Machine Learning | - Overseeing all ML development<br>- Developing machine learning models |
| Roman Makeev        | Fullstack        | - Integrating external APIs<br>- Developing core algorithms<br>- Future fullstack development for the website |
| Ilia Mitrokhin      | ML, Backend      | - Integrating LLMs into the application<br>- Developing the Telegram bot<br>- Potential backend development for the website |
| Anastasia Pichugina | ML, Fullstack    | - Integrating LLMs into the application<br>- Developing the Telegram bot<br>- Potential frontend development for the website |

### **Weekly Progress Report**

Our team did...

### **Challenges & Solutions**

...

### **Conclusions & Next Steps**

...

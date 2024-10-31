# CivicAlert 

CivicAlert is a mobile app built with Flutter that empowers users to report and upvote complaints about local issues. If a complaint reaches five or more upvotes, it is automatically forwarded to the appropriate government authorities, increasing the likelihood of action on community concerns. By leveraging Appwrite for backend services and a Python script for automated email notifications, CivicAlert ensures that community voices are amplified effectively.
## Project Contribution

- Developed the backend services using Appwrite.
- Implemented automated email notifications in Python to alert authorities when complaints reach a certain threshold of upvotes.

## Features

- **User-Generated Complaints**: Users can submit complaints with relevant details (title, description, location, images).
- **Community Feed**: Complaints are displayed in a feed view, ordered by upvotes, allowing users to support issues they care about.
- **Automated Government Notification**: A Python script, deployed on a server, continuously monitors the Appwrite database for changes in upvotes. When a complaint reaches five upvotes, it triggers an automated email notification to the government, ensuring timely awareness of popular community concerns.
- **Personal Complaint Management**: Users can track and view complaints they’ve submitted, monitoring issue progress and public support.

## File Structure

```
complaintsApp/
│
├── app.py                       # Main application file
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables
├── .gitignore                   # Git ignore file
└── README.md                    # Project documentation
```

## Run Commands

To run the application locally, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/ShreyasGandhi0607/complaintsApp.git
   cd complaintsApp
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up your environment variables in a `.env` file:

   ```
   MAIL_SERVER=smtp.your-email.com
   MAIL_USERNAME=your-email@example.com
   PASSWORD=your-email-password
   APPWRITE_PROJECT_ID=your-appwrite-project-id
   APPWRITE_API_KEY=your-appwrite-api-key
   APP_WRITE_DATABASE_ID=your-database-id
   APPWRITE_COMPLAINTS_COLLECTION_ID=your-complaints-collection-id
   APPWRITE_USERS_COLLECTION_ID=your-users-collection-id
   ```

5. Run the application:

   ```bash
   python app.py
   ```

## Deployed Link

- https://complaintsapp.onrender.com/process-complaint

### POST Request for Processing Complaints

To process a complaint, send a POST request to the deployed link with the following JSON body:

```json
{
  "complaint_id": "<YOUR_COMPLAINT_ID>"
}
```

## Contributing
If you would like to contribute to the CivicAlert project, please follow these steps:

- Fork the repository.
- Create a new branch for your feature or bug fix.
- Make your changes and test them thoroughly.
- Submit a pull request, explaining the changes you've made and why.


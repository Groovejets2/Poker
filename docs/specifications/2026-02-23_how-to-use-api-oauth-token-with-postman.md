> Why does the Postman setup have a blank token variable? I want to be able to use the Potman colection now in real
time?

● The token variable is intentionally blank - it gets filled automatically when you send the Login request! Let me
  show you how to use it in real-time right now:

  Quick Start: Using Postman Collection NOW

  Step 1: Import the Collection

  # File is at:
  backend/OpenClaw-Poker-API.postman_collection.json
  # OR
  docs/specifications/OpenClaw Poker Platform API.postman_collection.v1.1.json

  1. Open Postman
  2. Click "Import" button
  3. Select the JSON file
  4. Collection loads with blank {{token}} variable (this is normal!)

  ---
  Step 2: Start the API Server

  cd backend
  npm start

  You should see:
  TypeORM DataSource initialized successfully
  OpenClaw Poker API running on port 5000

  ---
  Step 3: Create a User Account (First Time Only)

  Send the "Register" request:

  Request:
  POST http://localhost:5000/api/auth/register

  Body (already in collection):
  {
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
  }

  Click "Send"

  Response (201 Created):
  {
    "user_id": 1,
    "username": "testuser",
    "message": "User created successfully"
  }

  ---
  Step 4: Login to Get JWT Token (Automatic!)

  Send the "Login" request:

  Request:
  POST http://localhost:5000/api/auth/login

  Body (already in collection):
  {
    "username": "testuser",
    "password": "password123"
  }

  Click "Send"

  Response (200 OK):
  {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6InRlc3R1c2VyIiwiaWF0IjoxNzA5NjExM
  jAwLCJleHAiOjE3MDk2MTQ4MDB9.abc123...",
    "user_id": 1,
    "username": "testuser",
    "expires_in": 3600
  }

  🎉 The token is NOW automatically saved!

  Look in the Postman Console (View → Show Postman Console) and you'll see:
  JWT Token saved! Expires in 3600 seconds
  All protected endpoints will now use this token automatically

  The {{token}} variable is now filled with the real JWT token!

  ---
  Step 5: Test Protected Endpoints (Token Auto-Applied!)

  Now try any protected endpoint - the token is automatically included:

  Example: Register for Tournament
  POST http://localhost:5000/api/tournaments/1/register

  Just click "Send" - the Authorization: Bearer {{token}} header is automatically added!

  ---
  Checking the Token Value

  To verify the token was saved:

  1. In Postman: Click the collection name → Variables tab
  2. Look at token variable - it should show the JWT value (not blank anymore)

  OR

  Click the eye icon (👁️) in top right → Collection Variables → See token value

  ---
  Why It Starts Blank

  The token must start blank because:
  1. You don't have a token until you login
  2. Each login generates a NEW token (expires after 1 hour)
  3. The Login request's test script automatically saves it:

  // This runs automatically after Login request succeeds
  if (pm.response.code === 200) {
      var jsonData = pm.response.json();
      pm.collectionVariables.set('token', jsonData.token);  // ← Saves token here!
  }

  ---
  If You Want to Manually Set a Token

  If you already have a token from somewhere else, you can manually set it:

  1. Click collection name
  2. Go to "Variables" tab
  3. Set token CURRENT VALUE to your JWT token
  4. Click "Save"

  ---
  Troubleshooting

  Problem: "No users exist yet"

  Solution: The database might be empty. Create the first user:
  # Send Register request first to create testuser
  POST /api/auth/register
  Body: {"username": "testuser", "password": "password123"}

  Problem: "Token not being applied to requests"

  Solution: Make sure protected endpoints have auth set to "Inherit auth from parent"
  - Click request → Authorization tab → Type: "Inherit auth from parent"

  Problem: "Token expired"

  Solution: Just send Login request again - new token will be saved automatically!

  ---
  Ready to Test Now?

  1. Start server: cd backend && npm start
  2. Send Register request (creates user)
  3. Send Login request (token auto-saved ✅)
  4. Use any protected endpoint (token auto-applied ✅)

  Try it now and let me know if the token saves correctly!

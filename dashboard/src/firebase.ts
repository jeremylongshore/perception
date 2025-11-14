import { initializeApp } from 'firebase/app'
import { getAuth } from 'firebase/auth'
import { getFirestore } from 'firebase/firestore'

const firebaseConfig = {
  apiKey: "AIzaSyBhVVxPp7g7vXv1XZ7pZ2L0q7YxPxUgXqM",
  authDomain: "perception-with-intent.firebaseapp.com",
  projectId: "perception-with-intent",
  storageBucket: "perception-with-intent.firebasestorage.app",
  messagingSenderId: "755584869357",
  appId: "1:755584869357:web:d5f7c3b8b4e6f9a8c4d5e6"
}

// Initialize Firebase
const app = initializeApp(firebaseConfig)

// Initialize services
export const auth = getAuth(app)
export const db = getFirestore(app)

export default app

import { initializeApp } from "https://www.gstatic.com/firebasejs/11.2.0/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/11.2.0/firebase-analytics.js";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

//web app's Firebase config,dont forget to fucking encrypt the api key 
const firebaseConfig = {
  apiKey: "AIzaSyA9v6b24QAj0wCvy7h_AxeW_LaHLFy4K0A",
  authDomain: "researchranker-ae250.firebaseapp.com",
  projectId: "researchranker-ae250",
  storageBucket: "researchranker-ae250.firebasestorage.app",
  messagingSenderId: "842803859783",
  appId: "1:842803859783:web:2ab3c04379fc2092d73c62",
  measurementId: "G-B5FTP27YFC"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const auth = getAuth(app);


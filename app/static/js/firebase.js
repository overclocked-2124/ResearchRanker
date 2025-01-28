
import { initializeApp } from "https://www.gstatic.com/firebasejs/11.2.0/firebase-app.js";
import{getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword} from "https://www.gstatic.com/firebasejs/11.2.0/firebase-auth.js"
import{getFirestore, setDoc, doc} from  "https://www.gstatic.com/firebasejs/11.2.0/firebase-firestore.js"
 // Your web app's Firebase configuration
 const firebaseConfig = {
   apiKey: "AIzaSyA9v6b24QAj0wCvy7h_AxeW_LaHLFy4K0A",
   authDomain: "researchranker-ae250.firebaseapp.com",
   projectId: "researchranker-ae250",
   storageBucket: "researchranker-ae250.firebasestorage.app",
   messagingSenderId: "842803859783",
   appId: "1:842803859783:web:1c20cf5671c2b7b2d73c62",
   measurementId: "G-7SH6FYE2ZQ"
 };
function showmessage(message, divId){
  var messageDiv = document.getElementById(divId);
  messageDiv.style.display="block";
  messageDiv.innerHTML=message;
}
 // Initialize Firebase
const app = initializeApp(firebaseConfig);
const signupbutn = document.getElementById('submitSignUp');

signupbutn.addEventListener('click',(event)=> {
  event.preventDefault();
  const email = document.getElementById('signUpEmail').value;
  const password = document.getElementById('signUpPwd').value;

  const auth=getAuth();
  const db =getFirestore();

  createUserWithEmailAndPassword(auth,email,password)
  .then((userCred)=>{
    const user = userCred.user
    const userdata = {
      email : email
    };
    showmessage('Account created successfully','signUpMessage')
    const docRef = doc(db,"users",user.uid);
    setDoc(docRef,userdata)
    .then(()=>{
      window.location.href="home.html";
    })
    .catch((error)=>{
      console.error("error writing document",error)
    })
  })
  .catch((error)=>{
    const errorCode=error.code;
    if(errorCode == 'auth/email-already-in-use'){
      showmessage("Email Address Already exists",signUpMessage)
    }
    else{
      showmessage("unable to create user",signUpMessage)
    }
  })
})

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

//sign-up
const signUpButton = document.getElementById('submitSignUp');

signUpButton.addEventListener('click',(event)=> {
  event.preventDefault();
  const email = document.getElementById('signUpEmail').value;
  const password = document.getElementById('signUpPwd').value;
  const Name = document.getElementById('signUpName').value;

  const auth=getAuth();
  const db =getFirestore();

  if (Name == "" ){
    showmessage("Name cannot be empty",'signUpMessage');
  }
  else{
  createUserWithEmailAndPassword(auth,email,password)
  .then((userCred)=>{
    const user = userCred.user
    const userdata = {
      email : email,
      name : Name
    };
    showmessage('Account created successfully','signUpMessage')
    const docRef = doc(db,"users",user.uid);
    setDoc(docRef,userdata)
    .then(()=>{
      window.location.href="authenticator.html";
    })
    .catch((error)=>{
      console.error("error writing document",error);
    })
  })
  .catch((error)=>{
    const errorCode=error.code;
    if(errorCode == 'auth/email-already-in-use'){
      showmessage("Email Address Already exists",'signUpMessage');
    }
    else{
      showmessage("unable to create user",'signUpMessage');
    }
  })
  }
})

//sign-in
const signinButton = document.getElementById("submitSignIn");

signinButton.addEventListener('click',(event)=>{
  event.preventDefault();
  const email = document.getElementById('signInEmail').value;
  const password = document.getElementById('signInPwd').value;
  const auth= getAuth();

  signInWithEmailAndPassword(auth,email,password)
  .then((userCred)=>{
    showmessage("login is successful",'signInMessage');
    const user =  userCred.user;
    localStorage.setItem("loggedInUserId",user.uid);
    window.location.href='home.html';
  })
  .catch((error)=>{
    const errorCode=error.code;
    if(errorCode=='auth/invalid-credential')
      showmessage('Incorrect Error or Password','signInMessage');
    else{
      showmessage('Account does no exist','signInMessage');
  }
})
})

const logOutButton = document.getElementById("Logout");

logOutButton.addEventListener('click',(event)=>{
  event.preventDefault();

})
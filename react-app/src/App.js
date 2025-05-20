//import logo from './logo.svg';
//import './App.css';
import React, { useState, useEffect } from 'react'

function App() {

  const [sendMessage, setSendMessage] = useState("")

  const onSubmit = async (e) => {
    //Prevents auto. page reloading
    e.preventDefault()

    const data = {sendMessage}
    const url = "http://127.0.0.1:5000/"

    const options = {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(data)
    }

    //Communication
    const response = await fetch(url, options)

    if(response.status !== 201 && response.status !== 200){
      const data = await response.json()
      alert(data.message)
    }
    else{
      console.log("Success! Sent: " + JSON.stringify(data))
    }
  }

  // TEXT INPUT FORM
  return (
    <div>

      <form onSubmit={onSubmit}>
        <label>
          Enter some text:
          <input type="text" name="sendMessage" value={sendMessage} onChange={(e) => setSendMessage(e.target.value)}></input>
        </label>
        <button type="submit">Submit</button>  
      </form>

    </div>
  );
}



export default App;

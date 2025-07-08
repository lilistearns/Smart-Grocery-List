
import React, { useState, useEffect } from 'react'

export function SignUp() {

    const [sendName, setSendName] = useState("")
    const [sendEmail, setSendEmail] = useState("")
    const [sendUsername, setSendUsername] = useState("")
    const [sendPassword, setSendPassword] = useState("")

    const onSubmit = async (e) => {
        //Prevents auto. page reloading
        e.preventDefault()

        const data = {sendName, sendEmail, sendUsername, sendPassword}
        const url = "http://127.0.0.1:5000/signup"

        const options = {
            credentials: "include",
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
            console.log("Account Sent: " + JSON.stringify(data))
            window.location.href = "/preferences"
        }
    }


    return (
        <div>

            <h1>Creating an Account:</h1>

            <form onSubmit={onSubmit}>
                <label>
                    Name:
                    <input type="text" name="sendName" value={sendName} onChange={(e) => setSendName(e.target.value)}></input>
                </label>
                <label>
                    Email:
                    <input type="email" name="sendEmail" value={sendEmail} onChange={(e) => setSendEmail(e.target.value)}></input>
                </label>
                <label>
                    Username:
                    <input type="text" name="sendUsername" value={sendUsername} onChange={(e) => setSendUsername(e.target.value)}></input>
                </label>
                <label>
                    Password:
                    <input type="password" name="sendPassword" value={sendPassword} onChange={(e) => setSendPassword(e.target.value)}></input>
                </label>
            <button type="submit">Submit</button>  
            </form>

        </div>
    );
}
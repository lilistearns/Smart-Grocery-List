
import React, { useState, useEffect } from 'react'
import classes from "../styles/signup_login.module.css"

export function SignUp() {

    const [sendName, setSendName] = useState("")
    const [sendEmail, setSendEmail] = useState("")
    const [sendUsername, setSendUsername] = useState("")
    const [sendPassword, setSendPassword] = useState("")

    const onSubmit = async (e) => {
        //Prevents auto. page reloading
        e.preventDefault()

        const data = {sendName, sendEmail, sendUsername, sendPassword}
        const url = "http://10.220.58.6:5000/signup"

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
        <div className={classes.container}>

            <p className={classes.header}>Creating an Account</p>

            <form onSubmit={onSubmit} className={classes.form}>
                <div className={classes.form_elements}>
                    <label>
                        <p>Name:</p>
                        <input type="text" name="sendName" value={sendName} onChange={(e) => setSendName(e.target.value)}></input>
                    </label>
                    <label>
                        <p>Email:</p>
                        <input type="email" name="sendEmail" value={sendEmail} onChange={(e) => setSendEmail(e.target.value)}></input>
                    </label>
                    <label>
                        <p>Username:</p>
                        <input type="text" name="sendUsername" value={sendUsername} onChange={(e) => setSendUsername(e.target.value)}></input>
                    </label>
                    <label>
                        <p>Password:</p>
                        <input type="password" name="sendPassword" value={sendPassword} onChange={(e) => setSendPassword(e.target.value)}></input>
                    </label>
                    <button type="submit" className={classes.button}>Submit</button>  

                    <p>Already have an account? <a href = "/login">Login</a></p>
                </div>
            </form>

        </div>
    );
}
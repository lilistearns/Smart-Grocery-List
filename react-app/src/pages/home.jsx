import React, { useState, useEffect } from 'react'
import "../styles/style.css"

export function Home() {
    const [email, setEmail] = useState([{}])

    const options = {
            credentials: "include",
            method: "GET",
        }

    useEffect(() => { 
            fetch("http://127.0.0.1:5000/", options)
            .then(response => response.json())
            .then(data => {setEmail(data)})
    }, [])

    const logout = async () => {
        const options = {
            credentials: "include",
            method: "POST",
        }

        const response = await fetch("http://127.0.0.1:5000/logout", options)
        window.location.reload()
    }


    if(email.email != null){
        return (
        <div>
            <h1>Logged in</h1>
            <h3>Email: {email.email}</h3>

            <button onClick={logout}>Logout</button> 
            
        </div>
    );
    }
    else{
        return (
        <div className='container'>
            <h1>Welcome to Smart Grocery List</h1>
            <p>A different way to grocery shop.</p>
            <a href = "/login"><button>Login</button></a>
            <a href = "/signup"><button>Sign Up</button></a>
        </div>
    );
    }
    
}

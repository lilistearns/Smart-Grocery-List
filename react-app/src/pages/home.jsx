import React, { useState, useEffect } from 'react'
import "../styles/style.css"
import classes from "../styles/home.module.css"

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

    // Send Logout Request
    const logout = async () => {
        const options = {
            credentials: "include",
            method: "POST",
        }

        const response = await fetch("http://127.0.0.1:5000/logout", options)
        window.location.reload()
    }


    // Logged in Home Display

    if(email.email != null){
        return (
        <div>
            <nav className={classes.loggedin_nav}>
                <h3 className={classes.user}>Welcome {email.email}!</h3>
                <h1 className={classes.header_title}>Smart Grocery List</h1>
                <button onClick={logout}>Logout</button>
            </nav>



        </div>
    );

    // Logged out Home Display

    }
    else{
        return (
        <div>
            <nav className={classes.loggedout_nav}>
                <a href = "/login"><button>Login</button></a>
                <a href = "/signup"><button>Sign Up</button></a>
            </nav>

            <div className={classes.container}>
                <p className={classes.title}>Welcome to Smart Grocery List</p>
                <h3 className={classes.subtitle}>A different way to grocery shop</h3>
                <p>Get the best deals in a fraction of the time and save time for what matters.</p>

                <div className={classes.process}>
                    <div className={classes.process_text}>
                        <h3>The process is simple:</h3>

                        <ol>
                            <li>Add grocery items to a list</li>
                            <li>Select grocery stores you shop at</li> 
                            <li>Select your preferences</li>
                            <li>Get a curated list of branded items and the cheapest place to buy them</li>
                        </ol>
                    </div>
                </div>
                
                <h2 className={classes.start}>Get Started</h2>
                <a href = "/signup"><button>Sign Up</button></a>

                <p className={classes.login}>Already have an account?</p>
                <a href = "/login">Login</a>
            </div>
            
        </div>
    );
    }
    
}

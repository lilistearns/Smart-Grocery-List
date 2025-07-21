import React, { useState, useEffect } from 'react'
import "../styles/style.css"
import classes from "../styles/home.module.css"

export function Home() {
    const [email, setEmail] = useState([{}])

    const options = {
            credentials: "include",
            method: "GET"
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

        await fetch("http://127.0.0.1:5000/logout", options)
        window.location.reload()
    }


    /* Recommenders */

    const [item, setItem] = useState("")
    const [foundItem, setFoundItem] = useState([])

    const [itemList, setItemList] = useState([])
    const [foundList, setFoundList] = useState([])

    const onSubmitItem = async (e) => {
        //Prevents auto. page reloading
        e.preventDefault()

        const data = {item}
        const url = "http://127.0.0.1:5000/findItem"

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

        console.log("Data: " + JSON.stringify(data))

        if(response.status !== 201 && response.status !== 200){
            const data = await response.json()
            alert(data.message)
        }
        else{
            const data = await response.json()
            //console.log("Result: " + JSON.stringify(data))
            setFoundItem(data)
            
        }
    }

    const onSubmitList = async (e) => {
        //Prevents auto. page reloading
        e.preventDefault()

        const data = {itemList}
        const url = "http://127.0.0.1:5000/findList"

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

        console.log("Data: " + JSON.stringify(data))

        if(response.status !== 201 && response.status !== 200){
            const data = await response.json()
            alert(data.message)
        }
        else{
            const data = await response.json()
            //console.log("Result: " + JSON.stringify(data))
            setFoundList(data)
        }
    }

    const itemGroup = foundItem.map(option => {
        return (<li className={classes.ml_output} key={option[2] /* Key is URL */}> 
                    <p className={classes.ml_option}>Store: {option[0]}</p>
                    <p className={classes.ml_option}>Price: {option[1]}</p>
                    <p className={classes.ml_option}>URL: <a href={option[2]}>Link</a></p>
                    <p className={classes.ml_option}>Product Name: {option[3]}</p>
                    <p className={classes.ml_option}>Quantity: {option[4]}</p>
                </li>)
    });

    const listGroup = foundList.map(option => {
        return (<li className={classes.ml_output} key={option[2] /* Key is URL */}>
                    <p className={classes.ml_option}>Store: {option[0]}</p>
                    <p className={classes.ml_option}>Price: {option[1]}</p>
                    <p className={classes.ml_option}>URL: <a href={option[2]}>Link</a></p>
                    <p className={classes.ml_option}>Product Name: {option[3]}</p>
                    <p className={classes.ml_option}>Quantity: {option[4]}</p>
                </li>)
    });


    function navigateUpdate(){
        window.location.href = "/update"
    }


    // Logged in Home Display

    if(email.email != null){
        return (
            <div className={classes.container}>
                <nav className={classes.loggedin_nav}>
                    <a href = "/update"><button className={classes.account}>Account</button></a>

                    {/* <button className={classes.account} onClick={navigateUpdate}>Account</button> */}
                    <h1 className={classes.header_title}>Smart Grocery List</h1>
                    <button onClick={logout}>Logout</button>
                </nav>

                <h3 className={classes.user}>Welcome {email.email}!</h3>


                {/* Item Search */}

                <h4 className={classes.ml_instructions}>This feature is for a single grocery item. You will recieve three different options. <br></br>Please enter your item.</h4>

                <form onSubmit={onSubmitItem}>
                    <label>
                        Item Search:
                        <input className={classes.ml_inputbox} type="text" name="item" value={item} onChange={(e) => setItem(e.target.value)}></input>
                    </label>
                <button type="submit">Submit</button>  
                </form>

                {foundItem.length !== 0 &&
                <ul>
                    {itemGroup}
                </ul>
                }


                <hr className={classes.line_divider}/>

                
                {/* List Search */}

                <h4 className={classes.ml_instructions}>This feature is for muliple grocery items.  You will recieve one option for each grocery item. <br></br>Please enter your items separated with a comma.</h4>

                <form onSubmit={onSubmitList}>
                    <label>
                        List Search:
                        <input className={classes.ml_inputbox} type="text" name="itemList" value={itemList} onChange={(e) =>{var temp = e.target.value.split(','); setItemList(temp.map(list => list.trim()))}}></input>
                    </label>
                <button type="submit">Submit</button>  
                </form>

                {foundList.length !== 0 &&
                <ul>
                    {listGroup}
                </ul>
                }

            </div>
        );
    }

    // Logged out Home Display

    else{
        return (
            <div className={classes.container}>
                <nav className={classes.loggedout_nav}>
                    <p className={classes.nav_title}>Smart Grocery List</p>
                    <div className={classes.nav_action}>
                        <a href = "/login"><button>Login</button></a>
                        <a href = "/signup"><button>Sign Up</button></a>
                    </div>
                    
                </nav>

                <div className={classes.content_container}>
                    <p className={classes.heading}>A New Way to Grocery Shop</p>
                    <p className={classes.sub_heading}>A grocery list that gives you the best deals in a <br></br> fraction of the time, so you can save time for what matters.</p>

                    <div className={classes.process}>
                            <ol>
                                <li>
                                    <p className={classes.process_header}>Select Your Preferences</p>
                                    <p className={classes.process_text}>Set factors such as how important quality, quantity, and price are to you. Only get results based on the grocery stores you shop at.</p>
                                </li>
                                <li>
                                    <p className={classes.process_header}>Pick Your Recommender</p>
                                    <p className={classes.process_text}>Select from an item or list recommender. Submit your grocery item(s). Get instant results.</p>
                                </li>
                                <li>
                                    <p className={classes.process_header}>Obtain Your Curated Results</p>
                                    <p className={classes.process_text}>Get a curated set of branded items and the best place to buy them based on your preferences.</p>
                                </li>
                            </ol>
                    </div>

                    <a href = "/signup"><button className={classes.get_started}>Get Started</button></a>

                    <p className={classes.already_account_text}>Already have an account?</p>
                    <a href = "/login">Login</a>

                </div>
                
            </div>
        );
    }
}

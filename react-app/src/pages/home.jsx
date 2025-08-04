import React, { useState, useEffect } from 'react'
import "../styles/style.css"
import classes from "../styles/home.module.css"
import { CartButton } from "../components/cartButton"
import { PastListsButton } from "../components/pastListButton";

export function Home() {
    const [email, setEmail] = useState([{}])

    const [cartSize, setCartSize] = useState(0)

    const fetchCartSize = async () => {
        try {
            const response = await fetch("http://10.220.58.6:5000/getCartSize", {
                method: "POST",
                credentials: "include",
            })
            if (!response.ok) throw new Error("Failed to fetch cart size")
            const size = await response.json()
            setCartSize(size)
        } catch (error) {
            console.error("Error fetching cart size:", error)
        }
    }

    useEffect(() => { 
        fetchCartSize()
    }, [])

    const options = {
        credentials: "include",
        method: "GET"
    }

    useEffect(() => { 
        fetch("http://10.220.58.6:5000/", options)
        .then(response => response.json())
        .then(data => {setEmail(data)})
    }, [])

    // Send Logout Request
    const logout = async () => {
        const options = {
            credentials: "include",
            method: "POST",
        }

        await fetch("http://10.220.58.6:5000/logout", options)
        window.location.reload()
    }

    /* Recommenders */
    const [item, setItem] = useState("")
    const [returnedItem, setReturnedItem] = useState([])

    const [itemList, setItemList] = useState([])
    const [returnedList, setReturnedList] = useState([])

    const [itemReject, setItemReject] = useState([])
    const [listReject, setListReject] = useState([])

    const [itemAccept, setItemAccept] = useState([])
    const [listAccept, setListAccept] = useState([])

    const [itemDisplay1, setItemDisplay1] = useState([])
    const [itemDisplay2, setItemDisplay2] = useState([])
    const [itemDisplay3, setItemDisplay3] = useState([])
    
    const [listDisplay, setListDisplay] = useState([])

    const onSubmitItem = async (e) => {
        e.preventDefault()

        const data = {item}
        const url = "http://10.220.58.6:5000/findItem"

        const options = {
            credentials: "include",
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        }

        const response = await fetch(url, options)

        if(response.status !== 201 && response.status !== 200){
            const data = await response.json()
            alert(data.message)
        }
        else{
            const data = await response.json()

            setItemDisplay1(data[0])
            setItemDisplay2(data[1])
            setItemDisplay3(data[2])

            data.splice(0, 3) // remove first three items
            setReturnedItem(data)
        }
    }

    const onSubmitList = async (e) => {
        e.preventDefault()

        const data = {itemList}
        const url = "http://10.220.58.6:5000/findList"

        const options = {
            credentials: "include",
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        }

        const response = await fetch(url, options)

        if(response.status !== 201 && response.status !== 200){
            const data = await response.json()
            alert(data.message)
        }
        else{
            const data = await response.json()
            setListDisplay(data[0])
            data.splice(0, 1)
            setReturnedList(data)
        }
    }

    // Reject Item Request
    useEffect(() => { 
        (async() => {
            if(itemReject.length !== 0){
                const data = {itemReject}
                const url = "http://10.220.58.6:5000/rejectItem"

                const options = {
                    credentials: "include",
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(data)
                }

                const response = await fetch(url, options)

                if(response.status !== 201 && response.status !== 200){
                    const data = await response.json()
                    alert(data.message)
                }
                else{
                    console.log("Rejected Item: " + JSON.stringify(data))
                }
            }
        })()
    }, [itemReject])

    // Reject List Request
    useEffect(() => { 
        (async() => {
            if(listReject.length !== 0){
                const data = {listReject}
                const url = "http://10.220.58.6:5000/rejectList"

                const options = {
                    credentials: "include",
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(data)
                }

                const response = await fetch(url, options)

                if(response.status !== 201 && response.status !== 200){
                    const data = await response.json()
                    alert(data.message)
                }
                else{
                    console.log("Rejected List: " + JSON.stringify(data))
                }
            }
        })()
    }, [listReject])

    // Accept Item Request
    useEffect(() => { 
        (async() => {
            if(itemAccept.length !== 0){
                const data = {itemAccept}
                const url = "http://10.220.58.6:5000/acceptItem"

                const options = {
                    credentials: "include",
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(data)
                }

                const response = await fetch(url, options)

                if(response.status !== 201 && response.status !== 200){
                    const data = await response.json()
                    alert(data.message)
                }
                else{
                    console.log("Accepted Item: " + JSON.stringify(data))
                }
            }
        })()
    }, [itemAccept])

    // Accept List Request
    useEffect(() => { 
        (async() => {
            if(listAccept.length !== 0){
                const data = {listAccept}
                const url = "http://10.220.58.6:5000/acceptList"

                const options = {
                    credentials: "include",
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(data)
                }

                const response = await fetch(url, options)

                if(response.status !== 201 && response.status !== 200){
                    const data = await response.json()
                    alert(data.message)
                }
                else{
                    console.log("Accepted List: " + JSON.stringify(data))
                }
            }
        })()
    }, [listAccept])

    function removeItemOption(displayNumber){
        if (returnedItem.length === 0){
            alert("No More Options")
        }
        else{
            if (displayNumber === 1){
                setItemReject(itemDisplay1)
                setItemDisplay1(returnedItem[0])
            }
            else if (displayNumber === 2){
                setItemReject(itemDisplay2)
                setItemDisplay2(returnedItem[0])
            }
            else{
                setItemReject(itemDisplay3)
                setItemDisplay3(returnedItem[0])
            }
            returnedItem.splice(0, 1)
        }
    }

    function removeListOption(){
        if (returnedList.length === 0){
            alert("No More Options")
        }
        else{
            setListReject(listDisplay)
            setListDisplay(returnedList[0])
            returnedList.splice(0, 1)
        }
    }

    function acceptItemOption(displayNumber) {
        if (displayNumber === 1) {
            setItemAccept(itemDisplay1);
        } else if (displayNumber === 2) {
            setItemAccept(itemDisplay2);
        } else {
            setItemAccept(itemDisplay3);
        }
        setItemDisplay1([]);
        setItemDisplay2([]);
        setItemDisplay3([]);
        setReturnedItem([]);

 
        fetchCartSize();
    }

    function acceptListOption() {
        setListAccept(listDisplay);
        setListDisplay([]);
        setReturnedList([]);

        fetchCartSize();
    }

    const listGroup = listDisplay.map(option => (
        <li className={classes.ml_option_content} key={option[2]}>
            <p className={classes.ml_option_content_details}>Store: {option[0]}</p>
            <p className={classes.ml_option_content_details}>Price: {option[1]}</p>
            <p className={classes.ml_option_content_details}>URL: <a href={option[2]}>Link</a></p>
            <p className={classes.ml_option_content_details}>Product Name: {option[3]}</p>
            <p className={classes.ml_option_content_details}>Quantity: {option[4]}</p>
        </li>
    ))

    if(email.email != null){
        return (
            <div className={classes.container_in}>
                <nav className={classes.loggedin_nav}>
                    <a href="/update"><button className={classes.account}>Account</button></a>
                    <h1 className={classes.header_title}>BudgetBasket</h1>
                    <div style={{ display: "flex", alignItems: "center", gap: "0.5rem" }}>
                        <CartButton cartSize={cartSize} />
                        <PastListsButton />
                        <button onClick={logout}>Logout</button>
                    </div>
                </nav>

                <p className={classes.user}>Welcome {email.email}!</p>

                <div className={classes.recommender_group_container}>
                    {}
                    <div className={classes.recommender_container}>
                        <h4 className={classes.ml_instructions}>
                            This feature is for a single grocery item. <br/>
                            You will receive three different options. <br/><br/>
                            Please enter your item.
                        </h4>

                        <form onSubmit={onSubmitItem}>
                            <label>
                                Item Search:
                                <input
                                    className={classes.ml_inputbox}
                                    type="text"
                                    name="item"
                                    value={item}
                                    onChange={(e) => setItem(e.target.value)}
                                />
                            </label>
                            <button type="submit">Submit</button>  
                        </form>

                        {(itemDisplay1.length !== 0 || itemDisplay2.length !== 0 || itemDisplay3.length !== 0) &&
                        <ul>
                            <li className={classes.ml_option} key={itemDisplay1[2]}>
                                <div className={classes.ml_option_top}>
                                    <p>Option 1</p>
                                    <div className={classes.test}>
                                        <button onClick={() => acceptItemOption(1)}>Accept</button>
                                        <button onClick={() => removeItemOption(1)} className={classes.reject_option_button}>Reject</button>
                                    </div>
                                </div>
                                <div className={classes.ml_option_content}>
                                    <p className={classes.ml_option_content_details}>Store: {itemDisplay1[0]}</p>
                                    <p className={classes.ml_option_content_details}>Price: {itemDisplay1[1]}</p>
                                    <p className={classes.ml_option_content_details}>URL: <a href={itemDisplay1[2]}>Link</a></p>
                                    <p className={classes.ml_option_content_details}>Product Name: {itemDisplay1[3]}</p>
                                    <p className={classes.ml_option_content_details}>Quantity: {itemDisplay1[4]}</p>
                                </div>
                            </li>
                            <li className={classes.ml_option} key={itemDisplay2[2]}>
                                <div className={classes.ml_option_top}>
                                    <p>Option 2</p>
                                    <div className={classes.test}>
                                        <button onClick={() => acceptItemOption(2)}>Accept</button>
                                        <button onClick={() => removeItemOption(2)} className={classes.reject_option_button}>Reject</button>
                                    </div>
                                </div>
                                <div className={classes.ml_option_content}>
                                    <p className={classes.ml_option_content_details}>Store: {itemDisplay2[0]}</p>
                                    <p className={classes.ml_option_content_details}>Price: {itemDisplay2[1]}</p>
                                    <p className={classes.ml_option_content_details}>URL: <a href={itemDisplay2[2]}>Link</a></p>
                                    <p className={classes.ml_option_content_details}>Product Name: {itemDisplay2[3]}</p>
                                    <p className={classes.ml_option_content_details}>Quantity: {itemDisplay2[4]}</p>
                                </div>
                            </li>
                            <li className={classes.ml_option} key={itemDisplay3[2]}>
                                <div className={classes.ml_option_top}>
                                    <p>Option 3</p>
                                    <div className={classes.test}>
                                        <button onClick={() => acceptItemOption(3)}>Accept</button>
                                        <button onClick={() => removeItemOption(3)} className={classes.reject_option_button}>Reject</button>
                                    </div>
                                </div>
                                <div className={classes.ml_option_content}>
                                    <p className={classes.ml_option_content_details}>Store: {itemDisplay3[0]}</p>
                                    <p className={classes.ml_option_content_details}>Price: {itemDisplay3[1]}</p>
                                    <p className={classes.ml_option_content_details}>URL: <a href={itemDisplay3[2]}>Link</a></p>
                                    <p className={classes.ml_option_content_details}>Product Name: {itemDisplay3[3]}</p>
                                    <p className={classes.ml_option_content_details}>Quantity: {itemDisplay3[4]}</p>
                                </div>
                            </li>
                        </ul>
                        }
                    </div>

                    <hr className={classes.recommender_line_divider}/>

                    {}
                    <div className={classes.recommender_container}>
                        <h4 className={classes.ml_instructions}>
                            This feature is for multiple grocery items. <br/>
                            You will receive one option with each grocery item. <br/><br/>
                            Please enter your items separated with a comma.
                        </h4>

                        <form onSubmit={onSubmitList}>
                            <label>
                                List Search:
                                <input
                                    className={classes.ml_inputbox}
                                    type="text"
                                    name="itemList"
                                    value={itemList}
                                    onChange={(e) => {
                                        var temp = e.target.value.split(',')
                                        setItemList(temp.map(list => list.trim()))
                                    }}
                                />
                            </label>
                            <button type="submit">Submit</button>  
                        </form>

                        {listDisplay.length !== 0 &&
                        <ul className={classes.ml_option}>
                            <div className={classes.ml_option_top}>
                                <p>Option</p>
                                <div className={classes.test}>
                                    <button onClick={() => acceptListOption()}>Accept</button>
                                    <button onClick={() => removeListOption()} className={classes.reject_option_button}>Reject</button>
                                </div>
                            </div>
                            {listGroup}
                        </ul>
                        }
                    </div>
                </div>
            </div>
        );
    }
    else{
        return (
            <div className={classes.container_out}>
                <nav className={classes.loggedout_nav}>
                    <p className={classes.nav_title}>BudgetBasket</p>
                    <div className={classes.nav_action}>
                        <a href = "/login"><button>Login</button></a>
                        <a href = "/signup"><button>Sign Up</button></a>
                    </div>
                </nav>

                <div className={classes.content_container}>
                    <p className={classes.heading}>A New Way to Grocery Shop</p>
                    <p className={classes.sub_heading}>A grocery list that gives you the best deals in a <br/> fraction of the time, so you can save time for what matters.</p>

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

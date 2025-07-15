import React, { useState, useEffect } from 'react'
import classes from "../styles/update.module.css"

export function Update() {
    // Determine if currently logged in
    const [currentEmail, setCurrentEmail] = useState([{}])
    
    const options = {
            credentials: "include",
            method: "GET"
        }

    useEffect(() => { 
            fetch("http://127.0.0.1:5000/", options)
            .then(response => response.json())
            .then(data => {setCurrentEmail(data)})
    }, [])

    // Set preferences
    const [settings, setSettings] = useState("account")

    const [name, setName] = useState("")
    const [email, setEmail] = useState("")
    const [username, setUsername] = useState("")

    const [qual, setQual] = useState("")
    const [price, setPrice] = useState("")
    const [quant, setQuant] = useState("")
    const [size, setSize] = useState("")
    const [diet, setDiet] = useState("")

    const [storeID1, setStoreID1] = useState("")
    const [storeID2, setStoreID2] = useState("")
    const [storeID3, setStoreID3] = useState("")
    const [storeID4, setStoreID4] = useState("")
    const [storeID5, setStoreID5] = useState("")

    const onSubmitStores = async (e) => {
        //Prevents auto. page reloading
        e.preventDefault()

        const data = {storeID1, storeID2, storeID3, storeID4, storeID5}
        const url = "http://127.0.0.1:5000/updateStores"

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
            console.log("Update Sent: " + JSON.stringify(data))
        }
    }

     const onSubmitPreferences = async (e) => {
        //Prevents auto. page reloading
        e.preventDefault()

        const data = {qual, price, quant}
        const url = "http://127.0.0.1:5000/updatePreferences"

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
            console.log("Update Sent: " + JSON.stringify(data))
        }
     }

     const onSubmitSize = async (e) => {
        //Prevents auto. page reloading
        e.preventDefault()

        const data = {size}
        const url = "http://127.0.0.1:5000/updateShoppingSize"

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
            console.log("Update Sent: " + JSON.stringify(data))
        }
     }

     const onSubmitDiet = async (e) => {
        //Prevents auto. page reloading
        e.preventDefault()

        const data = {diet}
        console.log(diet)
        const url = "http://127.0.0.1:5000/updateDiet"

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
            console.log("Update Sent: " + JSON.stringify(data))
        }
     }

     const onSubmitAccount = async (e) => {
     }

    function navigateHome(){
        window.location.href = "/"
    }


    // Logged in Display

    if(currentEmail.email != null){
        return(
            <div>

                <nav>
                    <button onClick={navigateHome}>Home</button>
                    <h1>Update Settings</h1>
                </nav>

                <div className={classes.radio} onChange={(e) => setSettings(e.target.value)}>
                    <div>
                        <label>
                            <input type="radio" name="settings" value="account" defaultChecked style={{color: 'red'}}></input>
                            Account
                        </label>
                    </div>
                    <div>
                        <label>
                            <input type="radio" name="settings" value="preferences"></input>
                            Preferences
                        </label>
                    </div>
                    <div>
                        <label>
                            <input type="radio" name="settings" value="stores"></input>
                            Stores
                        </label>
                    </div>
                </div>

                {settings === "account" &&
                <div>  
                    <form onSubmit={onSubmitAccount}>
                        <label>
                        Name:
                        <input type="text" name="name" value={name} onChange={(e) => setName(e.target.value)}></input>
                        </label>
                        <label>
                            Email:
                            <input type="email" name="email" value={email} onChange={(e) => setEmail(e.target.value)}></input>
                        </label>
                        <label>
                            Username:
                            <input type="text" name="username" value={username} onChange={(e) => setUsername(e.target.value)}></input>
                        </label>
                        <button >Change Password</button>
                    <button type="submit">Submit</button>  
                    </form>
                </div>
                }

                {settings === "preferences" &&
                <div>
                    
                    <form onSubmit={onSubmitPreferences}>
                        <label>
                            Quality:
                            <input type="range" name="qual" min="1" max="10" value={qual} onChange={(e) => setQual(e.target.value)}></input>
                            <p>Value: {qual}</p>
                        </label>
                        <label>
                            Price:
                            <input type="range" name="price" min="1" max="10" value={price} onChange={(e) => setPrice(e.target.value)}></input>
                            <p>Value: {price}</p>
                        </label>
                        <label>
                            Quantity:
                            <input type="range" name="quant" min="1" max="10" value={quant} onChange={(e) => setQuant(e.target.value)}></input>
                            <p>Value: {quant}</p>
                        </label>
                            
                    <button type="submit">Submit</button>  
                    </form>

                    <form onSubmit={onSubmitSize}>
                        <label>
                            Size:
                            <input type="number" name="size" value={size} onChange={(e) => setSize(e.target.value)}></input>
                        </label>
                    <button type="submit">Submit</button>  
                    </form>

                    <form onSubmit={onSubmitDiet}>
                        <label>
                        Diet:
                            <select name="diet" value={diet} onChange={(e) => setDiet(e.target.value)}>
                                <option value="No Diet">"No Diet"</option>
                                <option value="vegetarian">Vegetarian</option>
                                <option value="vegan">Vegan</option>
                                <option value="keto">Keto</option> 
                            </select>
                        </label>
                    <button type="submit">Submit</button> 
                    </form>
                
                </div>
                }

                {settings === "stores" &&
                <div> 
                    <form onSubmit={onSubmitStores}>
                        <label>
                            Store 1:
                            <input type="text" name="storeID1" value={storeID1} onChange={(e) => setStoreID1(e.target.value)}></input>
                        </label>
                        <label>
                            Store 2:
                            <input type="text" name="storeID2" value={storeID2} onChange={(e) => setStoreID2(e.target.value)}></input>
                        </label>
                        <label>
                            Store 3:
                            <input type="text" name="storeID3" value={storeID3} onChange={(e) => setStoreID3(e.target.value)}></input>
                        </label>
                        <label>
                            Store 4:
                            <input type="text" name="storeID4" value={storeID4} onChange={(e) => setStoreID4(e.target.value)}></input>
                        </label>
                        <label>
                            Store 5:
                            <input type="text" name="storeID5" value={storeID5} onChange={(e) => setStoreID5(e.target.value)}></input>
                        </label>
                    <button type="submit">Submit</button>  
                    </form>
                </div>
                }

            </div>
        )
    }

    // Not logged in; go to landing page

}
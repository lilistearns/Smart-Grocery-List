import React, { useState, useEffect } from 'react'
import classes from "../styles/update.module.css"

export function Update() {
    // Determine if currently logged in
    const [email, setEmail] = useState([{}])
    
    const options = {
            credentials: "include",
            method: "GET"
        }

    useEffect(() => { 
            fetch("http://10.220.58.6:5000/", options)
            .then(response => response.json())
            .then(data => {setEmail(data)})
    }, [])

    // Set preferences
    const [settings, setSettings] = useState("account")

    const [newName, setNewName] = useState("")
    const [newEmail, setNewEmail] = useState("")
    const [newPassword, setNewPassword] = useState("")

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
        const url = "http://10.220.58.6:5000/updateStores"

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
        const url = "http://10.220.58.6:5000/updatePreferences"

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
        const url = "http://10.220.58.6:5000/updateShoppingSize"

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
        const url = "http://10.220.58.6:5000/updateDiet"

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

    const onSubmitName = async (e) => {
    }

    const onSubmitEmail = async (e) => {
    }

    const onSubmitPassword = async (e) => {
    }
    

    // Logged in Display

    if(email.email != null){
        return(
            <div className={classes.container}>

                <nav className={classes.nav}>
                    <a href="/"><button>Home</button></a>
                    <p className={classes.nav_title}>Update Settings</p>
                </nav>

                <div className={classes.content_container}>
                    
                    <div className={classes.radio_container} onChange={(e) => setSettings(e.target.value)}>
                        <div className={classes.radio}>
                            <label>
                                <input type="radio" name="settings" value="account" defaultChecked style={{color: 'red'}}></input>
                                Account
                            </label>
                        </div>
                        <div className={classes.radio}>
                            <label>
                                <input type="radio" name="settings" value="preferences"></input>
                                Preferences
                            </label>
                        </div>
                        <div className={classes.radio}>
                            <label>
                                <input type="radio" name="settings" value="stores"></input>
                                Stores
                            </label>
                        </div>
                    </div>

                    <div className={classes.update_container}>

                        {settings === "account" &&
                        <div className={classes.account_container}>  
                            <form onSubmit={onSubmitName} className={classes.account_form}>
                                <label>
                                <p>Name:</p>
                                <input type="text" name="newName" value={newName} onChange={(e) => setNewName(e.target.value)} className={classes.other_inputs}></input>
                                </label>
                            <button type="submit">Update Name</button>  
                            </form>

                            <form onSubmit={onSubmitEmail} className={classes.account_form}>
                                <label>
                                    <p>Email:</p>
                                    <input type="email" name="newEmail" value={newEmail} onChange={(e) => setNewEmail(e.target.value)} className={classes.other_inputs}></input>
                                </label>

                            <button type="submit">Update Email</button>  
                            </form>

                            <form onSubmit={onSubmitPassword} className={classes.account_form}>
                                <label>
                                    <p>Password:</p>
                                    <input type="text" name="newPassword" value={newPassword} onChange={(e) => setNewPassword(e.target.value)} className={classes.other_inputs}></input>
                                </label>
                            <button >Update Password</button>
                            </form>
                        </div>
                        }

                        {settings === "preferences" &&
                        <div>
                            
                            <form onSubmit={onSubmitPreferences}>
                                <div>
                                    <p className={classes.scale_text_prompt}>On a scale of 1–10, how important are quality, price, and quantity?</p>
        
                                    <div className={classes.label_group}>
                                        <label>
                                            <p>Quality Value: {qual}</p>
                                            <input type="range" name="qual" min="1" max="10" value={qual} onChange={(e) => setQual(e.target.value)} className={classes.scale_slider}/>
                                        </label>
                                    </div>
        
                                    <div className={classes.label_group}>
                                        <label>
                                            <p>Price Value: {price}</p>
                                            <input type="range" name="price" min="1" max="10" value={price} onChange={(e) => setPrice(e.target.value)} className={classes.scale_slider}/>
                                        </label>
                                    </div>
        
                                    <div className={classes.label_group}>
                                        <label>
                                            <p>Quantity Value: {quant}</p>
                                            <input type="range" name="quant" min="1" max="10" value={quant} onChange={(e) => setQuant(e.target.value)} className={classes.scale_slider}/>
                                        </label>
                                    </div>
                                </div>
                                    
                            <button type="submit" className={classes.scale_button}>Update Scale</button>  
                            </form>

                            <hr></hr>

                            <form onSubmit={onSubmitSize}  className={classes.label_group}>
                                <label>
                                    Shopping Size:
                                    <input type="number" name="size" value={size} onChange={(e) => setSize(e.target.value)} className={classes.other_inputs}></input>
                                </label>
                            <button type="submit">Update Shopping Size</button>  
                            </form>

                            <hr></hr>

                            <form onSubmit={onSubmitDiet} className={classes.label_group}>
                                <label>
                                Diet:
                                    <select name="diet" value={diet} onChange={(e) => setDiet(e.target.value)} className={classes.other_inputs}>
                                        <option value="No Diet">No Diet</option>
                                        <option value="vegetarian">Vegetarian</option>
                                        <option value="vegan">Vegan</option>
                                        <option value="keto">Keto</option> 
                                    </select>
                                </label>
                            <button type="submit">Update Diet</button> 
                            </form>
                        
                        </div>
                        }

                        {settings === "stores" &&
                        <div className={classes.stores_container}> 
                            <form onSubmit={onSubmitStores} className={classes.form}>
                                <div className={classes.stores}>
                                    <label>
                                        Store 1:
                                        <select name="storeID1" value={storeID1} onChange={(e) => setStoreID1(e.target.value)} className={classes.store_inputs}>
                                            <option value="">Select a store</option>
                                            <option value="starmarket">Star Market</option>
                                            <option value="walmart">Walmart</option>
                                            <option value="shaws">Shaws</option>
                                            <option value="hannaford">Hannaford</option>
                                        </select>
                                    </label>
                                </div>
        
                                <div className={classes.stores}>
                                    <label>
                                        Store 2:
                                        <select name="storeID2" value={storeID2} onChange={(e) => setStoreID2(e.target.value)} className={classes.store_inputs}>
                                            <option value="">Select a store</option>
                                            <option value="starmarket">Star Market</option>
                                            <option value="walmart">Walmart</option>
                                            <option value="shaws">Shaws</option>
                                            <option value="hannaford">Hannaford</option>
                                        </select>
                                    </label>
                                </div>
        
                                <div className={classes.stores}>
                                    <label>
                                        Store 3:
                                        <select name="storeID3" value={storeID3} onChange={(e) => setStoreID3(e.target.value)} className={classes.store_inputs}>
                                            <option value="">Select a store</option>
                                            <option value="starmarket">Star Market</option>
                                            <option value="walmart">Walmart</option>
                                            <option value="shaws">Shaws</option>
                                            <option value="hannaford">Hannaford</option>
                                        </select>
                                    </label>
                                </div>
        
                                <div className={classes.stores}>
                                    <label>
                                        Store 4:
                                        <select name="storeID4" value={storeID4} onChange={(e) => setStoreID4(e.target.value)} className={classes.store_inputs}>
                                            <option value="">Select a store</option>
                                            <option value="starmarket">Star Market</option>
                                            <option value="walmart">Walmart</option>
                                            <option value="shaws">Shaws</option>
                                            <option value="hannaford">Hannaford</option>
                                        </select>
                                    </label>
                                </div>
        
                                <div className={classes.stores}>
                                    <label>
                                        Store 5:
                                        <select name="storeID5" value={storeID5} onChange={(e) => setStoreID5(e.target.value)} className={classes.store_inputs}>
                                            <option value="0">Select a store</option>
                                            <option value="starmarket">Star Market</option>
                                            <option value="walmart">Walmart</option>
                                            <option value="shaws">Shaws</option>
                                            <option value="hannaford">Hannaford</option>
                                        </select>
                                    </label>
                                </div>
        
                                <button type="submit">Submit Stores</button>
                            </form>
                        </div>
                        }
                    </div>
                </div>

            </div>
        )
    }

    // Not logged in; go to landing page

}
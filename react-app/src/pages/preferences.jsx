import React, { useState, useEffect } from 'react'
import classes from "../styles/preferences.module.css"

export function Preferences() {
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

    const [storesDone, setStoresDone] = useState(false)
    const [isLoading, setIsLoading] = useState(false)

    // Preferences
    const [qual, setQual] = useState("5")
    const [price, setPrice] = useState("5")
    const [quant, setQuant] = useState("5")
    const [size, setSize] = useState("0")
    const [diet, setDiet] = useState("No Diet")

    // Store IDs
    const [storeID1, setStoreID1] = useState("")
    const [storeID2, setStoreID2] = useState("")
    const [storeID3, setStoreID3] = useState("")
    const [storeID4, setStoreID4] = useState("")
    const [storeID5, setStoreID5] = useState("")

    const onSubmitPreferences = async (e) => {
        e.preventDefault()
        const data = {qual, price, quant, size, diet}
        const url = "http://127.0.0.1:5000/insertPreferences"

        const options = {
            credentials: "include",
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        }

        setIsLoading(true)
        const response = await fetch(url, options)

        if(response.status !== 201 && response.status !== 200){
            const data = await response.json()
            alert(data.message)
        } else {
            console.log("Account Sent: " + JSON.stringify(data))
            setIsLoading(false)
            window.location.href = "/"
            
        }
    }

    const onSubmitStores = async (e) => {
        e.preventDefault()
        const data = {storeID1, storeID2, storeID3, storeID4, storeID5}
        const url = "http://127.0.0.1:5000/insertStores"

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
        } else {
            console.log("Stores Sent: " + JSON.stringify(data))
            setStoresDone(true)
        }
    }

    if(email.email != null){
        return(
            <div className={classes.container}>
                {isLoading && 
                <div className={classes.loading_container}>
                    <p>Getting your account ready <br></br><br></br>One moment...</p>
                    <div className={classes.loading_icon}></div>
                </div>
                }
                {(storesDone && !isLoading) &&
                <div>
                    <h2>Please input your preferences:</h2>
                    
                    <form onSubmit={onSubmitPreferences} className={classes.form}>
                        <div>
                            <p className={classes.input_text_prompt}>On a scale of 1–10, how important are quality, price, and quantity?</p>

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

                        <div className={classes.size_diet_container}>
                            <p className={classes.input_text_prompt}>Please input shopping size and diet.</p>

                            <div className={classes.label_group}>
                                <label>
                                    Size:
                                    <input type="number" name="size" value={size} onChange={(e) => setSize(e.target.value)} className={classes.other_inputs}/>
                                </label>
                            </div>

                            <div className={classes.label_group}>
                                <label>
                                    Diet:
                                    <select name="diet" value={diet} onChange={(e) => setDiet(e.target.value)} className={classes.other_inputs}>
                                        <option value="No Diet">No Diet</option>
                                        <option value="vegetarian">Vegetarian</option>
                                        <option value="vegan">Vegan</option>
                                        <option value="keto">Keto</option>
                                    </select>
                                </label>
                            </div>
                        </div>

                        <button type="submit">Submit Preferences</button>
                    </form>
                </div>
                }

                {(!storesDone && !isLoading) &&
                <div>
                    <h2>Choose up to 5 preferred stores:</h2>
                    
                    <form onSubmit={onSubmitStores} className={classes.form}>
                        <div className={classes.stores_container}> 
                            <div className={classes.stores}>
                                <label>
                                    Store 1:
                                    <select name="storeID1" value={storeID1} onChange={(e) => setStoreID1(e.target.value)} className={classes.other_inputs}>
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
                                    <select name="storeID2" value={storeID2} onChange={(e) => setStoreID2(e.target.value)} className={classes.other_inputs}>
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
                                    <select name="storeID3" value={storeID3} onChange={(e) => setStoreID3(e.target.value)} className={classes.other_inputs}>
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
                                    <select name="storeID4" value={storeID4} onChange={(e) => setStoreID4(e.target.value)} className={classes.other_inputs}>
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
                                    <select name="storeID5" value={storeID5} onChange={(e) => setStoreID5(e.target.value)} className={classes.other_inputs}>
                                        <option value="0">Select a store</option>
                                        <option value="starmarket">Star Market</option>
                                        <option value="walmart">Walmart</option>
                                        <option value="shaws">Shaws</option>
                                        <option value="hannaford">Hannaford</option>
                                    </select>
                                </label>
                            </div>
                        </div>
                        <button type="submit">Submit Stores</button>
                    </form>
                </div>
                }
            </div>
        )
    }

    // Not logged in
    return <div>Not logged in</div>
}
import React, { useState, useEffect } from 'react'

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

    // Preferences
    const [qual, setQual] = useState("5")
    const [price, setPrice] = useState("5")
    const [quant, setQuant] = useState("5")
    const [size, setSize] = useState("0")
    const [diet, setDiet] = useState("vegetarian")

    // Store IDs
    const [storeID1, setStoreID1] = useState("")
    const [storeID2, setStoreID2] = useState("")
    const [storeID3, setStoreID3] = useState("")
    const [storeID4, setStoreID4] = useState("")
    const [storeID5, setStoreID5] = useState("")

    const onSubmit = async (e) => {
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

        const response = await fetch(url, options)

        if(response.status !== 201 && response.status !== 200){
            const data = await response.json()
            alert(data.message)
        } else {
            console.log("Account Sent: " + JSON.stringify(data))
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
        }
    }

    if(email.email != null){
        return(
            <div>
                <h1>Please input your preferences:</h1>

                <p>On a scale of 1–10, how important are quality, price, and quantity?</p>
                <form onSubmit={onSubmit}>
                    <label>
                        Quality:
                        <input type="range" name="qual" min="1" max="10" value={qual} onChange={(e) => setQual(e.target.value)} />
                        <p>Value: {qual}</p>
                    </label>
                    <label>
                        Price:
                        <input type="range" name="price" min="1" max="10" value={price} onChange={(e) => setPrice(e.target.value)} />
                        <p>Value: {price}</p>
                    </label>
                    <label>
                        Quantity:
                        <input type="range" name="quant" min="1" max="10" value={quant} onChange={(e) => setQuant(e.target.value)} />
                        <p>Value: {quant}</p>
                    </label>

                    <p>Please input shopping size and diet.</p>
                    <label>
                        Size:
                        <input type="number" name="size" value={size} onChange={(e) => setSize(e.target.value)} />
                    </label>
                    <label>
                        Diet:
                        <select name="diet" value={diet} onChange={(e) => setDiet(e.target.value)}>
                            <option value="No Diet">No Diet</option>
                            <option value="vegetarian">Vegetarian</option>
                            <option value="vegan">Vegan</option>
                            <option value="keto">Keto</option>
                        </select>
                    </label>
                    <button type="submit">Submit Preferences</button>
                </form>

                <h2>Choose up to 5 preferred stores:</h2>
                <form onSubmit={onSubmitStores}>
                    <label>
                        Store 1:
                        <select name="storeID1" value={storeID1} onChange={(e) => setStoreID1(e.target.value)}>
                            <option value="">Select a store</option>
                            <option value="starmarket">Star Market</option>
                            <option value="walmart">Walmart</option>
                            <option value="shaws">Shaws</option>
                            <option value="hannaford">Hannaford</option>
                        </select>
                    </label>
                    <label>
                        Store 2:
                        <select name="storeID2" value={storeID2} onChange={(e) => setStoreID2(e.target.value)}>
                            <option value="">Select a store</option>
                            <option value="starmarket">Star Market</option>
                            <option value="walmart">Walmart</option>
                            <option value="shaws">Shaws</option>
                            <option value="hannaford">Hannaford</option>
                        </select>
                    </label>
                    <label>
                        Store 3:
                        <select name="storeID3" value={storeID3} onChange={(e) => setStoreID3(e.target.value)}>
                            <option value="">Select a store</option>
                            <option value="starmarket">Star Market</option>
                            <option value="walmart">Walmart</option>
                            <option value="shaws">Shaws</option>
                            <option value="hannaford">Hannaford</option>
                        </select>
                    </label>
                    <label>
                        Store 4:
                        <select name="storeID4" value={storeID4} onChange={(e) => setStoreID4(e.target.value)}>
                            <option value="">Select a store</option>
                            <option value="starmarket">Star Market</option>
                            <option value="walmart">Walmart</option>
                            <option value="shaws">Shaws</option>
                            <option value="hannaford">Hannaford</option>
                        </select>
                    </label>
                    <label>
                        Store 5:
                        <select name="storeID5" value={storeID5} onChange={(e) => setStoreID5(e.target.value)}>
                            <option value="0">Select a store</option>
                            <option value="starmarket">Star Market</option>
                            <option value="walmart">Walmart</option>
                            <option value="shaws">Shaws</option>
                            <option value="hannaford">Hannaford</option>
                        </select>
                    </label>
                    <button type="submit">Submit Stores</button>
                </form>
            </div>
        )
    }

    // Not logged in
    return <div>Not logged in</div>
}
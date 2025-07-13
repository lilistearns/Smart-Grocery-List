import React, { useState, useEffect } from 'react'

/* Page accessed after account sign-up; updating preferences performed on update page */

export function Preferences() {
    // Determine if currently logged in
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

    // Set preferences; default values
    const [qual, setQual] = useState("5")
    const [price, setPrice] = useState("5")
    const [quant, setQuant] = useState("5")
    const [size, setSize] = useState("0")
    const [diet, setDiet] = useState("vegitarian")


    const onSubmit = async (e) => {
        //Prevents auto. page reloading
        e.preventDefault()

        console.log(qual, price, quant, size, diet)

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

        //Communication
        const response = await fetch(url, options)

        if(response.status !== 201 && response.status !== 200){
            const data = await response.json()
            alert(data.message)
        }
        else{
            console.log("Account Sent: " + JSON.stringify(data))
            window.location.href = "/"
        }
    }


    // Logged in Display

    if(email.email != null){
        return(
            <div>

                <h1>Please input your preferences:</h1>

                <p>On a scale of 1-10, how important are quality, price, and quantity?</p>
                <form onSubmit={onSubmit}>
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

                    <p>Please input shopping size and diet.</p>
                    <label>
                        Size:
                        <input type="number" name="size" value={size} onChange={(e) => setSize(e.target.value)}></input>
                    </label>
                    <label>
                        Diet:
                        <select name="diet" onChange={(e) => setDiet(e.target.value)}>
                            <option name="diet" value="vegitarian">Vegitarian</option>
                            <option name="diet" value="vegan">Vegan</option>
                            <option name="diet" value="keto">Keto</option>
                        </select>
                    </label>
                <button type="submit">Submit</button>  
                </form>

            </div>
        )
    }  


    // Not logged in; go to landing page

}

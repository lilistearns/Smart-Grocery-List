import React, { useState, useEffect } from 'react'
import classes from "../styles/home.module.css"
import { CartButton } from "../components/cartButton"
import { PastListsButton } from "../components/pastListButton";
const logout = async () => {
    const options = {
        credentials: "include",
        method: "POST",
    }

    await fetch("http://10.220.58.6:5000/logout", options)
    window.location.reload()
}
export function PastLists() {
    const [pageNumber, setPageNumber] = useState(1)
    const [listData, setListData] = useState([])
    const [noMore, setNoMore] = useState(false)

    const fetchPastList = async () => {
        const url = "http://10.220.58.6:5000/getPastList"
        const data = { pageNumber }

        const options = {
            credentials: "include",
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        }

        try {
            const response = await fetch(url, options)
            const contentType = response.headers.get("Content-Type")

            if (contentType && contentType.includes("application/json")) {
                const result = await response.json()
                setListData(result)
                setNoMore(false)
            } else {
                const text = await response.text()
                if (text === "No More Lists") {
                    setNoMore(true)
                    setListData([])
                }
            }
        } catch (error) {
            console.error("Failed to fetch past list:", error)
            setNoMore(true)
            setListData([])
        }
    }

    useEffect(() => {
        fetchPastList()
    }, [pageNumber])

    const handleNext = () => {
        setPageNumber(prev => prev + 1)
    }

    const handlePrevious = () => {
        if (pageNumber > 1) {
            setPageNumber(prev => prev - 1)
            setNoMore(false)
        }
    }

    const handleRestart = () => {
        setPageNumber(1)
        setNoMore(false)
    }

    const listGroup = listData.map((item, idx) => (
        <li className={classes.ml_option_content} key={item[2] + idx}>
            <p className={classes.ml_option_content_details}>Store: {item[0]}</p>
            <p className={classes.ml_option_content_details}>Price: {item[1]}</p>
            <p className={classes.ml_option_content_details}>
                URL: <a href={item[2]} target="_blank" rel="noopener noreferrer">Link</a>
            </p>
            <p className={classes.ml_option_content_details}>Product Name: {item[3]}</p>
            <p className={classes.ml_option_content_details}>Quantity: {item[4]}</p>
        </li>
    ))

    return (
        <div className={classes.container_in}>
                <nav className={classes.loggedin_nav}>
                    <a href="/update"><button className={classes.account}>Account</button></a>
                    <h1 className={classes.header_title}>BudgetBasket</h1>
                    <div style={{ display: "flex", alignItems: "center", gap: "0.5rem" }}>
                        <CartButton />
                        <PastListsButton />
                        <button onClick={logout}>Logout</button>
                    </div>
                </nav>

            <div className={classes.recommender_container}>
                {listData.length > 0 ? (
                    <ul className={classes.ml_option}>
                        <div className={classes.ml_option_top}>
                            <p>List #{pageNumber}</p>
                            <div>
                                <button onClick={handlePrevious} disabled={pageNumber === 1}>Previous</button>
                                <button onClick={handleNext}>Next</button>
                            </div>
                        </div>
                        {listGroup}
                    </ul>
                ) : (
                    <div className={classes.ml_instructions}>
                        {noMore ? (
                            <>
                                <p>No more lists to display.</p>
                                <button onClick={handleRestart}>Start Over</button>
                            </>
                        ) : (
                            <p>Loading...</p>
                        )}
                    </div>
                )}
            </div>
        </div>
    )
}

import React, { useEffect, useState } from "react";
import classes from "../styles/home.module.css";
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

export function CartPage() {
    const [cartData, setCartData] = useState([]);
    const [loading, setLoading] = useState(true);

    const fetchCart = async () => {
        try {
            const response = await fetch("http://10.220.58.6:5000/getCart", {
                method: "POST",
                credentials: "include"
            });
            if (!response.ok) throw new Error("Failed to fetch cart");
            const result = await response.json();
            setCartData(result);
        } catch (error) {
            console.error("Error fetching cart:", error);
        } finally {
            setLoading(false);
        }
    };

    const removeCartItem = async (item) => {
        try {
            const response = await fetch("http://10.220.58.6:5000/removeCartItem", {
                method: "POST",
                credentials: "include",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ cartItem: item })
            });
            if (response.ok) {
                setCartData(prev =>
                    prev.filter(i => JSON.stringify(i) !== JSON.stringify(item))
                );
            } else {
                console.error("Failed to remove item from cart");
            }
        } catch (error) {
            console.error("Error removing item:", error);
        }
    };

    useEffect(() => {
        fetchCart();
    }, []);

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
                {loading ? (
                    <p className={classes.ml_instructions}>Loading...</p>
                ) : cartData.length === 0 ? (
                    <p className={classes.ml_instructions}>Your cart is empty.</p>
                ) : (
                    <ul className={classes.ml_option}>
                        {cartData.map((item, idx) => (
                            <li className={classes.ml_option_content} key={item[2] + idx}>
                                <p className={classes.ml_option_content_details}>Category: {item[0]}</p>
                                <p className={classes.ml_option_content_details}>Price: {item[1]}</p>
                                <p className={classes.ml_option_content_details}>
                                    URL: <a href={item[2]} target="_blank" rel="noopener noreferrer">Link</a>
                                </p>
                                <p className={classes.ml_option_content_details}>Product: {item[3]}</p>
                                <p className={classes.ml_option_content_details}>Quantity: {item[4]}</p>
                                <button
                                    onClick={() => removeCartItem(item)}
                                    className={classes.reject_option_button}
                                >
                                    Remove
                                </button>
                            </li>
                        ))}
                    </ul>
                )}
            </div>
        </div>
    );
}

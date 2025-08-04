import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

export function CartButton() {
  const [cartSize, setCartSize] = useState(0);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchCartSize = async () => {
      try {
        const response = await fetch("http://10.220.58.6:5000/getCartSize", {
          method: "POST",
          credentials: "include",
        });
        if (!response.ok) throw new Error("Failed to fetch cart size");
        const size = await response.json();
        setCartSize(size);
      } catch (error) {
        console.error("Error fetching cart size:", error);
      }
    };

    fetchCartSize();
  }, []);

  return (
    <button onClick={() => navigate("/cart")} style={{ position: "relative" }}>
      🛒
      {cartSize > 0 && (
        <span
          style={{
            position: "absolute",
            top: "-8px",
            right: "-8px",
            backgroundColor: "red",
            color: "white",
            borderRadius: "50%",
            padding: "2px 6px",
            fontSize: "0.75rem",
          }}
        >
          {cartSize}
        </span>
      )}
    </button>
  );
}

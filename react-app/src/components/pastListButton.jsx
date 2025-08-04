import React from "react";
import { useNavigate } from "react-router-dom";

export function PastListsButton() {
  const navigate = useNavigate();

  return (
    <button
      onClick={() => navigate("/pastlists")}
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        position: "relative",
        backgroundColor: "#79E77F",
        color: "black",
        borderRadius: "12px", 
        width: "45px",
        height: "45px",
        fontSize: "1.2rem",
        fontWeight: "bold",
        border: "1px solid #ccc",
        cursor: "pointer",
        padding: 0,
      }}
    >
      📜
    </button>
  );
}
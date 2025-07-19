"use client";
import { useEffect, useState } from "react";
import ProductCard from '../components/ProductCard';

export default function ShirtPage() {
  const [shirts, setShirts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:8000/products/shirt")
      .then(res => res.json())
      .then(data => {
      console.log("API data", data);
      if (Array.isArray(data.results)) {
        setShirts(data.results);
      } else {
        setShirts([]);
      }
      setLoading(false);
    });
  }, []);

  return (
    <section className="results-section">
      <h3>เสื้อ (Shirt)</h3>
      {loading && <p>กำลังโหลด...</p>}
      <div className="product-grid">
        {shirts.map(product => (
          <ProductCard product={product} key={product.id} />
        ))}
        {/* {!loading && shirts.length === 0 && <p>ยังไม่มีรายการแนะนำ</p>} */}
      </div>
    </section>
  );
}

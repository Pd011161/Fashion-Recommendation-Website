"use client";
import { useState } from "react";

// แก้ไข type ให้ Product
type Product = {
  id: string;
  name: string;
  th_desc: string;
  url: string;
  // เพิ่ม field อื่นถ้ามี
};

// เปลี่ยน backend url ตรงนี้ถ้ารัน container backend คนละ port
const BACKEND_URL = "http://localhost:8000";

// ProductCard component
function ProductCard({ product }: { product: Product }) {
  return (
    <div className="product-card">
      <img src={product.url} alt={product.name} width={180} height={240} />
      <h3>{product.name}</h3>
      <p>{product.th_desc}</p>
    </div>
  );
}

export default function Home() {
  const [textQuery, setTextQuery] = useState("");
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null); // set เป็น string|null
  const [results, setResults] = useState<Product[]>([]);
  const [loading, setLoading] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);

  // --- API Calls ---
  async function handleTextSearch(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setResults([]);
    setHasSearched(true);
    try {
      const res = await fetch(`${BACKEND_URL}/recommend-by-text`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: textQuery }),
      });
      const data = await res.json();
      setResults(data.results || []);
    } catch (err) {
      alert("เกิดข้อผิดพลาดในการค้นหา (text)");
    }
    setLoading(false);
  }

  async function handleImageSearch(e: React.FormEvent) {
    e.preventDefault();
    if (!imageFile) return;
    setLoading(true);
    setResults([]);
    setHasSearched(true);
    try {
      const formData = new FormData();
      formData.append("file", imageFile);

      const res = await fetch(`${BACKEND_URL}/recommend-by-image`, {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      setResults(data.results || []);
    } catch (err) {
      alert("เกิดข้อผิดพลาดในการค้นหา (image)");
    }
    setLoading(false);
  }

  // ฟังก์ชัน handle preview รูปที่เลือก
  function handleImageInput(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0] || null;
    setImageFile(file);
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        if (typeof reader.result === "string") {
          setImagePreview(reader.result);
        } else {
          setImagePreview(null);
        }
      };
      reader.readAsDataURL(file);
    } else {
      setImagePreview(null);
    }
  }

  return (
    <main>
      <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Prompt:wght@400;500;700&display=swap" />

      <section className="hero">
        <h2>ค้นหาเสื้อผ้าในสไตล์ของคุณ</h2>
        <p>
          แนะนำเสื้อผ้าและกางเกงที่ตรงใจ <br />
          แค่พิมพ์คำบรรยายหรืออัปโหลดรูป
        </p>
      </section>

      <section className="search-section">
        <form onSubmit={handleTextSearch} className="text-search-form">
          <input
            type="text"
            placeholder="พิมพ์สไตล์หรือรายละเอียดเสื้อผ้าที่ต้องการ..."
            value={textQuery}
            onChange={e => setTextQuery(e.target.value)}
            className="input-text"
            required
          />
          <button type="submit" className="action-btn" disabled={loading}>
            {loading ? "กำลังค้นหา..." : "ค้นหาด้วยข้อความ"}
          </button>
        </form>
        <div className="divider">หรือ</div>
        <form onSubmit={handleImageSearch} className="image-search-form">
          <label className="upload-label">
            <input
              type="file"
              accept="image/*"
              onChange={handleImageInput}
              required
              className="input-file"
            />
            <span>📷 เลือกรูปภาพ</span>
          </label>
          <button type="submit" className="action-btn" disabled={loading}>
            {loading ? "กำลังค้นหา..." : "ค้นหาด้วยรูป"}
          </button>
        </form>
        {/* Preview รูปที่เลือก */}
        {imagePreview && (
          <div className="image-preview">
            <img src={imagePreview} alt="Preview" />
            <p>ตัวอย่างรูปที่เลือก</p>
          </div>
        )}
      </section>

      <section className="results-section">
        <h3>สินค้าแนะนำ</h3>
        {loading && <p className="fade-in">กำลังค้นหา...</p>}

        <div className="product-grid">
          {results.map(product => (
            <ProductCard product={product} key={product.id} />
          ))}
          {!loading && results.length === 0 && (
            <p>🛒 ยังไม่มีรายการแนะนำ</p>
          )}
        </div>
      </section>
    </main>
  );
}

export default function ProductCard({ product }) {
  // ฟังก์ชันสำหรับแปลง url ให้เหมาะกับการแสดงผล
  function getImageSrc(url) {
    // กรณีเป็น Google Drive URL (มี id=xxx)
    const driveMatch = url.match(/id=([a-zA-Z0-9_-]+)/);
    if (driveMatch) {
      const id = driveMatch[1];
      return `https://drive.google.com/thumbnail?id=${id}`;
    }
    // ถ้าเป็น Googleusercontent หรือ url ทั่วไป
    return url;
  }

  // fallback กรณีโหลดรูปไม่ได้
  function handleImgError(e) {
    e.target.src = '/images/placeholder.jpg'; // เปลี่ยน path ตามที่คุณเก็บรูป placeholder
  }

  return (
    <div className="product-card">
      <img
        src={getImageSrc(product.url)}
        alt={product.name}
        width={180}
        height={240}
        onError={handleImgError}
        style={{ objectFit: 'cover', borderRadius: '8px' }}
      />
      <h3>{product.name}</h3>
      <p>{product.th_desc}</p>
    </div>
  );
}

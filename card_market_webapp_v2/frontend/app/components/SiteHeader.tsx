import Link from 'next/link';
export default function SiteHeader(){return <header className="site-header"><div className="header-inner"><Link href="/" className="brand">CARD<span>MARKET</span></Link><nav><Link href="/search">Market</Link><Link href="/research">Research</Link><Link href="/about">Methodology</Link></nav><Link href="/search" className="header-cta">Search cards</Link></div></header>}

import React from 'react';

const Header: React.FC = () => {
    return (
        <header>
            <h1>自治会ウェブページ</h1>
            <nav>
                <ul>
                    <li><a href="/">ホーム</a></li>
                    <li><a href="/about">について</a></li>
                    <li><a href="/contact">お問い合わせ</a></li>
                </ul>
            </nav>
        </header>
    );
};

export default Header;
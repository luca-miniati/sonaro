"use client";

import { signIn } from "next-auth/react";

const Home = () => {
  return (
    <main className="h-screen">
      <button onClick={() => signIn()}>Log in with Spotify</button>
    </main>
  );
}

export default Home;

import NbaGraph from "@/components/NbaGraph";

export default function Home() {
  return (
    <div className="w-full h-screen">
      <div className="absolute top-4 left-4 z-10 bg-white/90 dark:bg-zinc-900/90 backdrop-blur-sm p-4 rounded-lg shadow-lg">
        <h1 className="text-2xl font-semibold text-black dark:text-zinc-50 mb-1">
          This is Jason's cool idea
        </h1>
        <p className="text-sm text-zinc-600 dark:text-zinc-400">
          Teammate network viz incoming
        </p>
        <p className="text-xs text-zinc-500 dark:text-zinc-500 mt-2">
          Click a player to see their teams. Click a team to see teammates.
        </p>
      </div>
      <NbaGraph initialPlayerId={2544} />
    </div>
  );
}

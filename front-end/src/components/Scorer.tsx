import React, { useEffect, useState } from "react";
import API from "./API";

const Scorer = () => {
    const [tallyBoard, setTallyBoard] = useState<{player: string, score: number}[]>();
    const [featuredPlayer, setFeaturedPlayer] = useState<string>("");
    const [breakdown, setBreakdown] = useState<{total: number, songs: {[songName: string]: {score: number, votes: number, players: number}}}>();

    useEffect(() => {
        API.score().then(response => {
            console.log("scored the game");
            API.getTally().then(response => setTallyBoard(response.tally_board));
        });
    }, []);

    const featurePlayer = (player: string) => (event: React.MouseEvent) => {
        event.preventDefault()
        setFeaturedPlayer(player);
        API.getPlayerDetails(player).then(response => setBreakdown(response.breakdown));
    }

    return <div>
        <ol>
            {tallyBoard?.map(score => <li onMouseOver={featurePlayer(score.player)}>
                {score.player} - {score.score}
            </li>)}
        </ol>
        <div>
            {featuredPlayer}
            {breakdown?.total}
            {Object.entries(breakdown?.songs || {}).map(([song, detail]) => <div>{song}: {detail.score} from {detail.votes} votes and {detail.players} players guessing</div>)}
        </div>
    </div>;
}

export default Scorer;
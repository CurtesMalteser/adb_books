import Lottie from "lottie-react";
import lightAnimationData from '../../assets/lotties/calm_light.json';
import darkAnimationData from '../../assets/lotties/calm_dark.json';
import { useEffect, useState } from "react";
import './Loader.css';
import { Container } from "react-bootstrap";
import { isDarkModeSelector } from "../dark-mode/darkModeSlice";
import { useAppSelector } from "../../app/hooks";

function Loader() {

    const messages = [
        "Take a deep breath…",
        "Patience is a virtue…",
        "A moment of calm…",
        "Breathe in, breathe out…",
        "Every page has its time…",
        "Enjoy this quiet pause…",
        "A journey of words begins with a breath…",
        "Slow down, let your mind wander…",
        "Moments of stillness are precious…"
    ];

    const secondaryMessage = "Your next moment of tranquility is on its way...";

    const [currentMessage, setCurrentMessage] = useState(messages[0]);
    const [messageIndex, setMessageIndex] = useState(0);

    const isDarkMode = useAppSelector(isDarkModeSelector);

    const animationData = () => isDarkMode ? darkAnimationData : lightAnimationData;

    useEffect(() => {
        const messageInterval = setInterval(() => {
            setMessageIndex((prevIndex) => (prevIndex + 1) % messages.length);
        }, 4000);

        return () => clearInterval(messageInterval);
    }, [messages.length]);

    useEffect(() => {
        setCurrentMessage(messages[messageIndex]);
    }, [messageIndex, messages]);

    return (
        <Container className="text-center my-4" >
            <h2 className="d-flex justify-content-center text-secondary">{currentMessage}</h2>
            <div className="lottie-container">
                <Lottie
                    className="lottie-animation"
                    animationData={animationData()}
                    loop={true}
                    autoplay={true}
                    rendererSettings={
                        {
                            preserveAspectRatio: "xMidYMid slice"
                        }
                    }
                />
            </div>
            <h4 className="d-flex justify-content-center text-secondary">{secondaryMessage}</h4>
        </Container>
    );
}

export default Loader;
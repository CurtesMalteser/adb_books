import { useEffect, useRef, useState } from "react";
import { Card, Button, Form } from "react-bootstrap";

const TokenCard = ({ token }: { token: string | null }) => {
    const [copied, setCopied] = useState(false);
    const textareaRef = useRef<HTMLTextAreaElement>(null);

    const handleCopy = () => {
        const copyTimeout = 2000;
        navigator.clipboard.writeText(token ?? "");
        setCopied(true);
        setTimeout(() => setCopied(false), copyTimeout);
    };

    const adjustTextareaHeight = () => {
        if (textareaRef.current) {
            textareaRef.current.style.height = "auto"; // Reset height to auto first
            textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
        }
    };

    useEffect(() => {
        adjustTextareaHeight();
    }, [token]);

    return (
        <Card className="mb-4">
            <Card.Header><b>Token</b></Card.Header>
            <Card.Body>
                <Form.Control
                    as="textarea"
                    ref={textareaRef}
                    readOnly
                    value={token ?? ""}
                    style={{
                        fontFamily: "monospace",
                        whiteSpace: "pre-wrap",
                        overflow: "hidden",
                        resize: "none",
                    }}
                    onInput={adjustTextareaHeight}
                />
                <Button
                    variant={copied ? "success" : "primary"}
                    onClick={handleCopy}
                    className="mt-3"
                >
                    {copied ? "Copied!" : "Copy"}
                </Button>
            </Card.Body>
        </Card>
    );
};

export default TokenCard;

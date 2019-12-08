import GetAnnounce,MessageSender,ProcessText
def main():
    g = GetAnnounce.GetAnnounce("")
    m = MessageSender.MessageSender("serverchan")
    m.config({'SCKEY':'SCU59621Tfe85588030e0a45116714e3b47fd35d85d74d3e91354b'})
    g.createCache()
    cache = g.get()
    for i in cache:
        print(i)
        p = ProcessText.ProcessText(i)
        m.send(p.getFullTextMD())
    while True:
        cache = g.freshCache()
        if cache is not None:
            for i in cache:
                p = ProcessText.ProcessText(i)
                m.send(p.getFullTextMD())

def test():
    return

#test()
main()
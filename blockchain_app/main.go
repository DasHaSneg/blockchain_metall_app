package main

import (
	"flag"
	"fmt"
	"github.com/pkg/errors"
	"github.com/spf13/viper"
	abci "github.com/tendermint/tendermint/abci/types"
	cfg "github.com/tendermint/tendermint/config"
	tmflags "github.com/tendermint/tendermint/libs/cli/flags"
	"github.com/tendermint/tendermint/libs/log"
	nm "github.com/tendermint/tendermint/node"
	"github.com/tendermint/tendermint/p2p"
	"github.com/tendermint/tendermint/privval"
	"github.com/tendermint/tendermint/proxy"
	app "go/src/MyDiplomProject/diplomstore"
	"time"

	//"github.com/go-kit/kit/log/level"
	"os"
	"os/signal"
	"path/filepath"
	"syscall"
)

var configFile, bd_dir, perpeer, rpcadress string
var empty bool

func init() {
	flag.StringVar(&configFile, "config", "$HOME/config/config.toml", "Path to config.toml")
	flag.BoolVar(&empty, "empty", true, "Set this to false to only produce blocks when there are txs or when the AppHash changes")
	flag.StringVar(&perpeer, "per_peer", "", "Set persistent peers")
	flag.StringVar(&rpcadress, "rpc_adr", "tcp://127.0.0.1:26657", "Set listen address for rpc")

}

func main() {
	bd_dir := filepath.Dir(filepath.Dir(bd_dir))
	application := app.NewApplication(bd_dir)
	flag.Parse()
	node, err := newTendermint(application, configFile)
	if err != nil {
		fmt.Fprintf(os.Stderr, "%v", err)
		os.Exit(2)
	}
	err = node.OnStart()
	if err != nil {
		fmt.Fprintf(os.Stderr, "%v", err)
		os.Exit(2)
	}
	defer func() {
		node.OnStop()
		node.Wait()
	}()
	c := make(chan os.Signal, 1)
	signal.Notify(c, os.Interrupt, syscall.SIGTERM)
	<-c
	os.Exit(0)
}

func newTendermint(app abci.Application, configFile string) (*nm.Node, error) {
	// read config
	config := cfg.DefaultConfig()
	config.RootDir = filepath.Dir(filepath.Dir(configFile))
	viper.SetConfigFile(configFile)
	if err := viper.ReadInConfig(); err != nil {
		return nil, errors.Wrap(err, "viper failed to read config file")
	}
	if err := viper.Unmarshal(config); err != nil {
		return nil, errors.Wrap(err, "viper failed to unmarshal config")
	}
	if err := config.ValidateBasic(); err != nil {
		return nil, errors.Wrap(err, "config is invalid")
	}

	config.TxIndex.IndexAllKeys = true
	config.Consensus.CreateEmptyBlocks = empty
	config.P2P.PersistentPeers = perpeer
	config.RPC.ListenAddress = rpcadress
	if empty == true {
		seconds, _ := time.ParseDuration("30s")
		config.Consensus.CreateEmptyBlocksInterval = seconds
	}

	// create logger
	logger := log.NewTMLogger(log.NewSyncWriter(os.Stdout))
	var err error
	logger, err = tmflags.ParseLogLevel(config.LogLevel, logger, cfg.DefaultLogLevel())
	if err != nil {
		return nil, errors.Wrap(err, "failed to parse log level")
	}
	// read private validator
	pv := privval.LoadFilePV(
		config.PrivValidatorKeyFile(),
		config.PrivValidatorStateFile(),
	)
	// read node key
	nodeKey, err := p2p.LoadNodeKey(config.NodeKeyFile())
	if err != nil {
		return nil, errors.Wrap(err, "failed to load node's key")
	}
	// create node
	node, err := nm.NewNode(
		config,
		pv,
		nodeKey,
		proxy.NewLocalClientCreator(app),
		nm.DefaultGenesisDocProviderFunc(config),
		nm.DefaultDBProvider,
		nm.DefaultMetricsProvider(config.Instrumentation),
		logger)
	if err != nil {
		return nil, errors.Wrap(err, "failed to create new Tendermint node")
	}
	return node, nil
}

import numpy
import spead64_48 as spead
import logging
import sys

#logging.basicConfig(level=logging.INFO)
PORT = 8888


def receive():
    print 'RX: Initializing...'

    t = spead.TransportUDPrx(PORT)
    ig = spead.ItemGroup()
    for heap in spead.iterheaps(t):
        #print spead.readable_heap(heap)
        ig.update(heap)
        print 'Got heap:', ig.heap_cnt
        for name in ig.keys():
            print '   ', name
            item = ig.get_item(name)
            print '      Description: ', item.description
            print '           Format: ', item.format
            print '            Shape: ', item.shape
            print '            Value: ', ig[name]
    print 'RX: Done.'


def transmit():
    print 'TX: Initializing...'
    tx = spead.Transmitter(spead.TransportUDPtx('127.0.0.1', PORT, rate=1e9))
    ig = spead.ItemGroup()

    ig.add_item(name='Var1', description='Description for Var1',
        shape=[], fmt=spead.mkfmt(('u',32),('u',32),('u',32)),
        init_val=(1,2,3))
    tx.send_heap(ig.get_heap())
    ig['Var1'] = (4,5,6)
    tx.send_heap(ig.get_heap())

    data = numpy.arange(100000*4000).astype(numpy.uint32); data.shape = (100000,4000)
    ig.add_item(name='Var2', description='Description for Var2',
        shape=[100000,4000], ndarray=data)
    ig['Var2'] = data
    tx.send_heap(ig.get_heap())

    tx.end()
    print 'TX: Done.'

if sys.argv[-1] == 'tx':
    transmit()
elif sys.argv[-1] == 'rx':
    receive()
else:
    raise ValueError('Argument must be rx or tx')

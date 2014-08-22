using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using uPLibrary.Networking.M2Mqtt;
using uPLibrary.Networking.M2Mqtt.Messages;

namespace Sub_Ring
{
    class Program
    {
        static void Main(string[] args)
        {
            MqttClient client = new MqttClient("test.mosquitto.org");

            client.MqttMsgPublishReceived += client_MqttMsgPublishReceived;
            string[] topics = {"protosystemdemo/doorbell/ring"};
            byte[] qosLevels = { MqttMsgBase.QOS_LEVEL_AT_MOST_ONCE};
            client.Subscribe(topics,qosLevels);

            client.Connect(Guid.NewGuid().ToString());

            Console.ReadLine();

        }

        static void client_MqttMsgPublishReceived(object sender, MqttMsgPublishEventArgs e)
        {
            string message = Encoding.UTF8.GetString(e.Message);
            if (message.Equals("1"))
                Console.WriteLine("Someone is at the front door");
            if (message.Equals("2"))
                Console.WriteLine("Someone is at the back door");
        }

    }
}
